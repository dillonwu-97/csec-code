<?php
function xor_encrypt($in) {
    // these two dont work
    // $key= '{"show password":"no", "bgcolor"=>"#ffffff"}';
    // $key = {"showpassword":"no","bgcolor":"#ffffff"}; 
    $key = json_encode(array( "showpassword"=>"no", "bgcolor"=>"#ffffff")); 
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}

function xor_encrypt2($in) {
    // $key = json_encode(array( "showpassword"=>"yes", "bgcolor"=>"#ffffff")); 
    $key = 'qw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8j';
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}
$data = json_encode(array( "showpassword"=>"yes", "bgcolor"=>"#ffffff"));

// echo json_encode(array( "showpassword"=>"no", "bgcolor"=>"#ffffff"));
// echo xor_encrypt(base64_decode('ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSEV4sFxFeaAw='));
echo base64_encode(xor_encrypt2($data));

  
