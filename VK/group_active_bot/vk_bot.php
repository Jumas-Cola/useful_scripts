<?php
include "vk_api.php";

// **********CONFIG**************
$config = json_decode(file_get_contents('config.json'));
$GROUP_TOKEN = $config->GROUP_TOKEN;
$CONFIRMATION_TOKEN = $config->CONFIRMATION_TOKEN;
$SECRET_KEY = $config->SECRET_KEY;
$TEXT_FILE = $config->TEXT_FILE;
$FIRST_COMMENTS = $config->FIRST_COMMENTS;
$COMMENT_CHANCE =  $config->COMMENT_CHANCE;
$V = $config->V;
// ******************************

if (!isset($_REQUEST)) {
    return;
}

$data = json_decode(file_get_contents('php://input'));

if (strcmp($data->secret, $SECRET_KEY) !== 0 && strcmp($data->type, 'confirmation') !== 0) {
    return;
}

$vk = new vk_api($GROUP_TOKEN, $V);

switch ($data->type) {
    case 'confirmation':
        exit($CONFIRMATION_TOKEN);

    case 'wall_reply_new':
        if (rand(1, 100) >= $COMMENT_CHANCE) {
            $vk->sendOK();
            break;
        }
        $reply_to_comment = $data->object->id;
        $post_id = $data->object->post_id;
        $owner_id = $data->object->owner_id;
        $from_id = $data->object->from_id;
        if ($from_id == $owner_id) {
            $vk->sendOK();
            break;
        }
        $texts = file($TEXT_FILE);
        $resp = $vk->request('wall.createComment', [
                    'owner_id' => $owner_id,
                    'post_id' => $post_id,
                    'from_group' => -$owner_id,
                    'message' => trim($texts[array_rand($texts)]),
                    'reply_to_comment' => $reply_to_comment,
                  ]);
        $vk->sendOK();
        break;

    case 'wall_post_new':
        $marked_as_ads = $data->object->marked_as_ads;
        if ($marked_as_ads) {
            $vk->sendOK();
            break;
        }
        $post_id = $data->object->id;
        $owner_id = $data->object->owner_id;
        $texts = file($FIRST_COMMENTS);
        $resp = $vk->request('wall.createComment', [
                    'owner_id' => $owner_id,
                    'post_id' => $post_id,
                    'from_group' => -$owner_id,
                    'message' => trim($texts[array_rand($texts)]),
                  ]);
        $vk->sendOK();
        break;
}
