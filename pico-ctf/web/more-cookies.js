const url = 'http://mercury.picoctf.net:10868/'
const opts = {
    headers: {
        cookie: 'auth_name=Q2wvZUVTd2VBRXJXMU04Uy9vRHlhU3R3ZzQ1Wi85QUNobFRDRkdEWDVtVFNIUEd6SWFTb2ZnZ2ZERnM5TzVaVm1yeDZBZmJJT0hnWDU0dHlTL2o4QjFIMU9VMHVDYUl5UEszdFo3MzF0QWw4OXZPaCs0eHlmT1luR3U3L1dVdkk='
    }
}

async function make_req() {

    const result = await fetch(url, opts)
    const txt = await result.text()
    console.log(txt)

}

make_req()
