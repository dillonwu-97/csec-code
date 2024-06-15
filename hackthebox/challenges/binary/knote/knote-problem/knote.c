#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/device.h>
#include <linux/mutex.h>
#include <linux/fs.h>
#include <linux/slab.h>
#include <linux/uaccess.h>

#define DEVICE_NAME "knote"
#define CLASS_NAME "knote"

MODULE_AUTHOR("r4j");
MODULE_DESCRIPTION("Secure your secrets in the kernelspace");
MODULE_LICENSE("GPL");

static DEFINE_MUTEX(knote_ioctl_lock);

// used for communicating with the device using i/o?
// so if I want to do something like knote_create, then I need to make a call to KNOTE_ENCRYPT / DECRYPT I guess?
// and that would go into the cmd argument, arg contains a pointer 
static long knote_ioctl(struct file *file, unsigned int cmd, unsigned long arg);

static int major;
static struct class *knote_class  = NULL;
static struct device *knote_device = NULL;
static struct file_operations knote_fops = {
    .unlocked_ioctl = knote_ioctl
};

struct knote {
    char *data;
    size_t len;
    void (*encrypt_func)(char *, size_t);
    void (*decrypt_func)(char *, size_t);
};

struct knote_user {
    unsigned long idx;
    char * data;
    size_t len;
};

enum knote_ioctl_cmd {
    KNOTE_CREATE = 0x1337,
    KNOTE_DELETE = 0x1338,
    KNOTE_READ = 0x1339,
    KNOTE_ENCRYPT = 0x133a,
    KNOTE_DECRYPT = 0x133b
};

struct knote *knotes[10]; // array of 10 pointers in memory 

void knote_encrypt(char * data, size_t len) {
    int i;
    for(i = 0; i < len; ++i)
        data[i] ^= 0xaa;
}

void knote_decrypt(char *data, size_t len) {
    knote_encrypt(data, len);
}

static long knote_ioctl(struct file *file, unsigned int cmd, unsigned long arg) {
    mutex_lock(&knote_ioctl_lock);
    struct knote_user ku;

    // copy a block of data from user space 
    // copy_from_user(to, input arg, something)
    // is it just 8 bytes of data that is being copied?
    //    <-- No; we are instead copying a pointer in memory containing the struct data 
    // struct file is part of linux and it represents information about an open file 
    // how is copy_from_user different if smep/smap is disabled?
    if(copy_from_user(&ku, (void *)arg, sizeof(struct knote_user)))
        return -EFAULT;
    switch(cmd) {
        // vulnerability is here 
        case KNOTE_CREATE:
            if(ku.len > 0x20 || ku.idx >= 10)
                // no unlock done here
                // so maybe there is some race condition that we have to exploit?
                // what happens if mutex is never unlocked? then another thread waits forever 
                //
                return -EINVAL;
            char *data = kmalloc(ku.len, GFP_KERNEL); // GFP_KERNEL specifies allocation context / behavior 
            // do something like knote create 
            // kmalloc 32 bytes
            knotes[ku.idx] = kmalloc(sizeof(struct knote), GFP_KERNEL);
            if(data == NULL || knotes[ku.idx] == NULL) {
                mutex_unlock(&knote_ioctl_lock);
                return -ENOMEM;
            }

            knotes[ku.idx]->data = data;
            knotes[ku.idx]->len = ku.len;

            // so we need copy_from_user to pass with invalid data?
            // i.e. kmalloc() does not return null, we set data and length, then call free() on some bad data?
            // copy_from_user returns 0 on success, so non zero = failed copy = call kfree() 
            // so need to make copy_from_user fail 
            // so the knote struct stuff is in kernel land i think ?
            // copy to ku.idx->data from ku.data  
            if(copy_from_user(knotes[ku.idx]->data, ku.data, ku.len)) {
                kfree(knotes[ku.idx]->data);
                kfree(knotes[ku.idx]);
                mutex_unlock(&knote_ioctl_lock);
                return -EFAULT;
            }
            knotes[ku.idx]->encrypt_func = knote_encrypt; 
            knotes[ku.idx]->decrypt_func = knote_decrypt; 
            break;
        case KNOTE_DELETE:
            // I guess there is a check here to make sure that ku.idx is not empty 
            if(ku.idx >= 10 || !knotes[ku.idx]) {
                mutex_unlock(&knote_ioctl_lock);
                return -EINVAL;
            }
            // no check so we could do something like call kfree() twice on the same freed memory 
            kfree(knotes[ku.idx]->data);
            kfree(knotes[ku.idx]);
            knotes[ku.idx] = NULL;
            break;
        case KNOTE_READ:
            if(ku.idx >= 10 || !knotes[ku.idx] || ku.len > knotes[ku.idx]->len) {
                mutex_unlock(&knote_ioctl_lock);
                return -EINVAL;
            }
            if(copy_to_user(ku.data, knotes[ku.idx]->data, ku.len)) {
                mutex_unlock(&knote_ioctl_lock);
                return -EFAULT;
            }
            break;
        // do an encryption
        case KNOTE_ENCRYPT:
            if(ku.idx >= 10 || !knotes[ku.idx]) {
                mutex_unlock(&knote_ioctl_lock);
                return -EINVAL;
            }
            knotes[ku.idx]->encrypt_func(knotes[ku.idx]->data, knotes[ku.idx]->len);
            break;
        // do a decryption
         case KNOTE_DECRYPT:
            if(ku.idx >= 10 || !knotes[ku.idx]) {
                mutex_unlock(&knote_ioctl_lock);
                return -EINVAL;
            }
            knotes[ku.idx]->decrypt_func(knotes[ku.idx]->data, knotes[ku.idx]->len);
            break;
        default:
            mutex_unlock(&knote_ioctl_lock);
            return -EINVAL;
    }
    mutex_unlock(&knote_ioctl_lock);
    return 0;
}

static int __init init_knote(void) {
    major = register_chrdev(0, DEVICE_NAME, &knote_fops);
    if(major < 0)
        return -1;

    knote_class = class_create(THIS_MODULE, CLASS_NAME);
    if (IS_ERR(knote_class)) {
        unregister_chrdev(major, DEVICE_NAME);
        return -1;
    }

    knote_device = device_create(knote_class, 0, MKDEV(major, 0), 0, DEVICE_NAME);
    if (IS_ERR(knote_device))
    {
        class_destroy(knote_class);
        unregister_chrdev(major, DEVICE_NAME);
        return -1;
    }

    return 0;
}

static void __exit exit_knote(void)
{
    device_destroy(knote_class, MKDEV(major, 0));
    class_unregister(knote_class);
    class_destroy(knote_class);
    unregister_chrdev(major, DEVICE_NAME);
}

module_init(init_knote);
module_exit(exit_knote);
