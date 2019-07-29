<?php

$config = array(
  'token' => '',
  'v' => '5.73',
  'text' => ' %s %s Принимаю всеееееех в друзья! %s %s
    %s %s У меня неееееет подписчиков! %s %s
    %s %s Добавляйтееееееее меня! %s %s',
  'groups' => array(
              '34985835',
              '8337923',
              '33764742',
              '39130136',
              '59721672',
              '24261502',
              '94946045',
              '34985835',
              '8337923',
              '33764742',
              '39130136',
              '99839307',
              '59721672',
              '46258034',
              '47350356',
              '62584051',
              '74738426',
              '55897568',
              '39673900',
              '101933932',
              '61413825',
              '68486191',
              '35990996',
              '47484197',
              '59221166',
              '43606620',
              '42590964',
              '76862936',
              '77541446',
              '76672098',
              '111977624',
              '62445889',
              '111548821',
              '141765627',
              '110762291',
              '63013736',
              '59583855',
              '111417272',
              '135842087',
              '41211515',
              '68999007',
              '74738426',
              '39673900',
              '62584051',
              '47350356',
              '55897568',
              '61413825',
              '24370682',
              '32538224',
              '62919013',
              '59833666',
// Добавленные группы
              '50189240',
              '53611139',
              '86843576',
              '72566600',
              '118548409',
              '102777394',
              '160308044',
              '36534224',
              '38097482',
              '89093386',
              '32863460',
              '105645450',
              '10190856',
              '94946045',
              '83836947',
              '59622376',
              '119694346',
              '38074299',
              '61175725',
              '119693332',
              '135315925',
              '56578271',
              '63023089',
              '60637173',
              '43688291',
              '74350037',
              '78552709',
              '93947385',
              '60841267',
              '58541895',
              '56907236',
              '77941885',
          ),
    'emoji' => array(
              '😊',
              '😃',
              '😉',
              '😆',
              '😜',
              '😋',
              '😍',
              '😎',
              '😒',
              '😏',
              '😌',
              '😄',
              '😇',
              '🌱',
              '🌲',
              '🌳',
              '🌴',
              '🌵',
              '🌿',
              '🍀',
              '🍁',
              '🍂',
              '🍃',
              '🗽',
              '🗼',
              '🗻',
              '🎴',
              '🎑'
          ),
);

date_default_timezone_set('Europe/Moscow');
$time1 = date('H');
if ($time1 > 5 or $time1 < 3)
{

    #Список групп
    $gr = $config['groups'];
    //
    #Список смайликов
    $sm = $config['emoji'];

    $v = $config['v'];

    #Делаем онлайн
    $api = vk_method('account.setOnline', array());

    #немного спим
    usleep(500);

    #Добавляем в друзья заявки
    $api = vk_method('friends.getRequests', array(
      'count' => 1000,
    ));
    $items = $api['response']['items'];
    foreach ($items as $item) {
      $resp = vk_method('friends.add', array(
        'user_id' => $item,
      ));
    }

    #немного спим
    usleep(500);

    #Удаляем исходящие заявки
    $api = vk_method('friends.getRequests', array(
      'out' => 1,
      'count' => 1000,
    ));
    $items = $api['response']['items'];
    foreach ($items as $item) {
      $resp = vk_method('friends.delete', array(
        'user_id' => $item,
      ));
    }

    #немного спим
    usleep(500);

    #Рассылка рекламных постов по группам
    $f_strs = substr_count($config['text'], '%s');
    foreach ($gr as $group) {
      $resp = vk_method('wall.post', array(
        'owner_id' => '-' . $group,
        'message' => sprintf_arr($config['text'], array_fill(1, $f_strs, $sm[array_rand($sm)])),
        'from_group' => 0,
      ));

      //Вывод информации о рассылке
      if (isset($resp['response']['post_id'])) {
        $post = $resp['response']['post_id'];
        echo '<a href="https://vk.com/wall-' . $group . '_' . $post . '">' . $group . '_' . $post . '</a></br>';
      } else {
        echo 'Не удалось сделать пост: ' . $group . '</br>';
      }

      usleep(500);
    }
}

// Отправка запроса через curl
function curl($url, $post = false)
{
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
    curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36");
    if ($post)
    {
        curl_setopt($ch,

        CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $post);
    }
    curl_setopt($ch, CURLOPT_COOKIEJAR, "./cookiee3");
    curl_setopt($ch, CURLOPT_COOKIEFILE, "./cookiee3");
    $response = curl_exec($ch);
    curl_close($ch);
    return $response;
}

// Вызов метода VK API
function vk_method($method, $request_params)
{
    global $config;
    $request_params['access_token'] = $config['token'];
    $request_params['v'] = $config['v'];
    $get_params = http_build_query($request_params);
    $url = sprintf('https://api.vk.com/method/%s?%s', $method, $get_params);
    $response = json_decode(curl($url), true);
    return $response;
}

// Форматирование строки массивом
function sprintf_arr($format, $arr)
{
    return call_user_func_array('sprintf', array_merge((array)$format, $arr));
}

?>
