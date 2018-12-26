<?php
/*
Скрипт для автоматического постинга из альбома на стену группы. Запускать через cron
*/

$config = [
  'owner_id'   => -169696294, // id группы куда постить
  'album_owner' => 408736104, // id владельца альбома с картинками
  'album_id' => 'profile', // id альбома с картинками
  'message' => '#anime

  Источник: pinterest.com', // текст поста
  'access_token' => '', // токен доступа пользователя
  'offset' => '',
  'v' => '5.92',
];

$vk_config_json = get_offset();
$config['offset'] = $vk_config_json->offset;

for ($i = 0; $i < 5; $i++) {
    try {
        // получение ссылки на очередную картинку из альбома
        $request_params = [
          'owner_id' => $config['album_owner'],
          'album_id' => $config['album_id'],
          'rev' => 0,
          'offset' => $config['offset'],
          'count' => 1,
          'access_token' => $config['access_token'],
          'v' => $config['v'],
        ];
        $response = vk_method('photos.get', $request_params);
        $oid = $response->response->items[0]->owner_id;
        $count = $response->response->count;
        $media_id = $response->response->items[0]->id;

        // размещение картинки на стене сообщества
        $request_params = [
          'owner_id' => $config['owner_id'],
          'from_group' => '1',
          'message' => $config['message'],
          'attachments' => 'photo' . $oid . '_' . $media_id . '',
          'access_token' => $config['access_token'],
          'v' => $config['v'],
        ];
        $response = vk_method('wall.post', $request_params);
        $file_json = json_decode(file_get_contents('vk_config.json'));
        $file_json->offset++; // увеличение отступа на 1
        if ($file_json->offset >= $count) {
          $file_json->offset = 0;
        }
        file_put_contents('vk_config.json', json_encode($file_json));
        break;
    } catch (Exception $e) {
        echo $e->getMessage();
        sleep(1.3*i);
    }
}


function get_offset($file = 'vk_config.json')
{
    if (is_file($file) && file_get_contents($file)) {
        $file_json = json_decode(file_get_contents($file));
        $offset = $file_json->offset;
    } else {
        $offset = 0;
    }
    $vk_config_json = json_encode([
      'offset' => $offset,
    ]);
    file_put_contents($file, $vk_config_json);
    return json_decode($vk_config_json);
}

function vk_method($method, $request_params)
{
  $get_params = http_build_query($request_params);
  $url = sprintf('https://api.vk.com/method/%s?%s', $method, $get_params);
  $response = json_decode(file_get_contents($url));
  return $response;
}
