<?php
/*
Скрипт для автоматического постинга из альбома на стену группы. Запускать через cron
Если уже есть токен - то вставить его в файл vk_config.json
Если нет токена - то введите логин и пароль и он будет получен автоматически

clientID = "2274003"                      //VK for Android app client_id
clientSecret = "hHbZxrka2uZ6jB1inYsH"     //VK for Android app client_secret
clientID = "3697615"                      //VK for Windows app client_id
clientSecret = "AlVXZFMUqyrnABp8ncuU"     //VK for Windows app client_secret
clientID = "3140623"                        //VK for iPhone app client_id
clientSecret = "VeWdmVclDCtn6ihuP1nt"       //VK for iPhone app client_secret
*/

$config = [
  // в эти поля нужно вставить свои данные
  'login' => 'login',
  'password' => 'password',
  'owner_id'   => -169696294, // id группы куда постить
  'album_owner' => -168416289, // id владельца альбома с картинками
  'album_id' => 255171792, // id альбома с картинками
  'message' => '', // текст поста
  // это лучше не трогать
  'client_id' => 3697615,
  'client_secret' => 'AlVXZFMUqyrnABp8ncuU',
  'access_token' => '',
  'offset' => '',
  'v' => '5.92',
];
// получение токена и отступа или чтение их из файла, если он существует и не пуст
$vk_config_json = get_config($config['client_id'], $config['client_secret'], $config['login'], $config['password']);
$config['access_token'] = $vk_config_json->access_token;
$config['offset'] = $vk_config_json->offset;

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
  $get_params = http_build_query($request_params);
  $response = json_decode(file_get_contents('https://api.vk.com/method/photos.get?' . $get_params));
  $oid = $response->response->items[0]->owner_id;
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
  $get_params = http_build_query($request_params);
  $response = json_decode(file_get_contents('https://api.vk.com/method/wall.post?' . $get_params));
  $file_json = json_decode(file_get_contents('vk_config.json'));
  $file_json->offset++; // увеличение отступа на 1
  file_put_contents('vk_config.json', json_encode($file_json));
} catch (Exception $e) {
  echo $e->getMessage();
}

// Получает access token и offset и сохраняет их в файл, если файл ещё не создан
function get_config($client_id, $client_secret, $login, $password) {
  $file = 'vk_config.json';
  if (is_file($file) && file_get_contents($file)) {
    $file_json = json_decode(file_get_contents($file));
    $accessToken = $file_json->access_token;
    $offset = $file_json->offset;
  } else {
    $getToken = json_decode(file_get_contents('https://oauth.vk.com/token?grant_type=password&client_id='.$client_id.'&client_secret='.$client_secret.'&username='.$login.'&password='.$password.'&v=5.37&2fa_supported=1'));
    $accessToken = $getToken->access_token;
    $offset = 0;
  }
  $vk_config_json = json_encode([
    'access_token' => $accessToken,
    'offset' => $offset,
  ]);
  file_put_contents($file, $vk_config_json);
  return json_decode($vk_config_json);
}
