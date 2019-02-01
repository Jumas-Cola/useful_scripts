<?php
/*
  Скрипт для автоматического выхода из бесед. Запускать через cron (vk.com)
*/
$config = [
  'exceptions' => [441, 56], // id бесед, которые не надо удалять
  'access_token' => '',
  'v' => '5.92',
];

$vk = new vk($config);
$response = $vk->method('messages.getConversations');
foreach ($response['response']['items'] as $item) {
    $local_id = $item['conversation']['peer']['local_id'];
    if (!in_array($local_id, $vk->exceptions)) {
        $vk->method('messages.removeChatUser', [
          'chat_id' => $local_id,
          'member_id' => $vk->id,
        ]);
        $vk->method('messages.deleteConversation', [
          'peer_id' => 2000000000 + $local_id,
        ]);
    };
}


class vk
{
    public function __construct($config)
    {
        $this->access_token = $config['access_token'];
        $this->v = $config['v'];
        $this->exceptions = $config['exceptions'];
        $this->id = $this->method('users.get')['response'][0]['id'];
    }

    public function method($method, $request_params=[])
    {
        $request_params['access_token'] = $this->access_token;
        $request_params['v'] = $this->v;
        $get_params = http_build_query($request_params);
        $url = sprintf('https://api.vk.com/method/%s?%s', $method, $get_params);
        $response = json_decode(file_get_contents($url), true);
        return $response;
    }
}
