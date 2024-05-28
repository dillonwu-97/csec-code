call fclose() on a stream object
so create a fake stream object to call close with 
really early version of libc as well 

so we can create a fake vtable pointer that points to the next chunk in memory as wel 


https://elixir.bootlin.com/glibc/glibc-2.23/A/ident/fclose
https://elixir.bootlin.com/glibc/glibc-2.23/source/include/stdio.h#L127
    -> _IO_new_fclose
https://elixir.bootlin.com/glibc/glibc-2.23/source/libio/iofclose.c#L34
    -> _IO_new_fclose definition

struct: https://elixir.bootlin.com/glibc/glibc-2.23/source/libio/libio.h#L241


need to replace a function pointer with win() and should be golden 
_chain points to list of pointers so maybe we can use that 


check _vtable_offset 




struct _IO_FILE_plus
{
  _IO_FILE file;
  const struct _IO_jump_t *vtable;
};


struct _IO_FILE {
  int _flags;		/* High-order word is _IO_MAGIC; rest is flags. */
#define _IO_file_flags _flags

  /* The following pointers correspond to the C++ streambuf protocol. */
  /* Note:  Tk uses the _IO_read_ptr and _IO_read_end fields directly. */
  char* _IO_read_ptr;	/* Current read pointer */
  char* _IO_read_end;	/* End of get area. */
  char* _IO_read_base;	/* Start of putback+get area. */
  char* _IO_write_base;	/* Start of put area. */
  char* _IO_write_ptr;	/* Current put pointer. */
  char* _IO_write_end;	/* End of put area. */
  char* _IO_buf_base;	/* Start of reserve area. */
  char* _IO_buf_end;	/* End of reserve area. */
  /* The following fields are used to support backing up and undo. */
  char *_IO_save_base; /* Pointer to start of non-current get area. */
  char *_IO_backup_base;  /* Pointer to first valid character of backup area */
  char *_IO_save_end; /* Pointer to end of non-current get area. */

  struct _IO_marker *_markers;

  struct _IO_FILE *_chain;

  int _fileno;
#if 0
  int _blksize;
#else
  int _flags2;
#endif
  _IO_off_t _old_offset; /* This used to be _offset but it's too small.  */

#define __HAVE_COLUMN /* temporary */
  /* 1+column number of pbase(); 0 is unknown. */
  unsigned short _cur_column;
  signed char _vtable_offset; <-- vtable_offset returns this value
  char _shortbuf[1];

  /*  char* _save_gptr;  char* _save_egptr; */

  _IO_lock_t *_lock;
#ifdef _IO_USE_OLD_IO_FILE
};


unlink attack is also possible?
not entirely sure
i can also put something onto the free list
but the goal is just to call win() so is there something easier?

so create fake jump table immediately after the vtable struct to pass all of the checks 
call JUMP1 with the win() function?
ok goal is to call _IO_FINISH() which should point to _finish




$1 = {
  file = {
    _flags = -72537977,
    _IO_read_ptr = 0x601103 <_IO_2_1_stdout_@@GLIBC_2.2.5+131> "",
    _IO_read_end = 0x601103 <_IO_2_1_stdout_@@GLIBC_2.2.5+131> "",
    _IO_read_base = 0x601103 <_IO_2_1_stdout_@@GLIBC_2.2.5+131> "",
    _IO_write_base = 0x601103 <_IO_2_1_stdout_@@GLIBC_2.2.5+131> "",
    _IO_write_ptr = 0x601103 <_IO_2_1_stdout_@@GLIBC_2.2.5+131> "",
    _IO_write_end = 0x601103 <_IO_2_1_stdout_@@GLIBC_2.2.5+131> "",
    _IO_buf_base = 0x601103 <_IO_2_1_stdout_@@GLIBC_2.2.5+131> "",
    _IO_buf_end = 0x601104 <_IO_2_1_stdout_@@GLIBC_2.2.5+132> "",
    _IO_save_base = 0x0,
    _IO_backup_base = 0x0,
    _IO_save_end = 0x0,
    _markers = 0x0,
    _chain = 0x601160 <_IO_2_1_stdin_@@GLIBC_2.2.5>,
    _fileno = 1,
    _flags2 = 0,
    _old_offset = -1,
    _cur_column = 0,
    _vtable_offset = 0 '\000',
    _shortbuf = "",
    _lock = 0x7ffff7fa97e0 <_IO_stdfile_1_lock>,
    _offset = -1,
    _codecvt = 0x0,
    _wide_data = 0x7ffff7fa7880 <_IO_wide_data_1>,
    _freeres_list = 0x0,
    _freeres_buf = 0x0,
    __pad5 = 0,
    _mode = -1,
    _unused2 = '\000' <repeats 19 times>
  },
  vtable = 0x7ffff7fa44a0 <_IO_file_jumps>
}

