<?php
/*
Скрипт для автоматического постинга рекламных постов. Запускать через cron
*/
$config = [
  'album_owner' => 456490164, // id владельца альбома с картинками
  'album_id' => 254187932, // id альбома с картинками
  'message' => "@id456490164(Добавляйся в друзья!)", // текст поста
  'groups' => [ // группы, где пиарить
    -161158169,
    -129331704,
  ],
  'access_token' => '', // токен доступа пользователя
  'v' => '5.92',
];


$response = vk_method('photos.get', [
  'owner_id' => $config['album_owner'],
  'album_id' => $config['album_id'],
]);
$count = $response->response->count;
$response = vk_method('photos.get', [
  'owner_id' => $config['album_owner'],
  'album_id' => $config['album_id'],
  'offset' => random_int(0, $count-1),
  'count' => 1,
]);
$owner_id = $response->response->items[0]->owner_id;
$id = $response->response->items[0]->id;
$attachments = sprintf('photo%s_%s', $owner_id, $id);
$response = vk_method('wall.post', [
  'owner_id' => $config['groups'][array_rand($config['groups'])],
  'from_group' => 0,
  'message' => $config['message'],
  'attachments' => $attachments,
]);

function vk_method($method, $request_params)
{
    global $config;
    $request_params['access_token'] = $config['access_token'];
    $request_params['v'] = $config['v'];
    $get_params = http_build_query($request_params);
    $url = sprintf('https://api.vk.com/method/%s?%s', $method, $get_params);
    $response = json_decode(file_get_contents($url));
    return $response;
}
