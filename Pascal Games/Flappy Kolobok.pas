uses graphABC;


type
  circle = record
    x: integer;
    y: integer;
    rad: integer;
    vel_x: integer;
    vel_y: integer;
  end;

type
  block = record
    x: integer;
    size_x: integer;
    center: integer;
  end;

var
  k: circle; 
  accel := 1;
  score := 0;
  game_speed := 5;
  difficulty := 100;
  count_walls := 8;
  rand_range := 40;
  block_arr: array of block;
  b_size_x := trunc(WindowWidth / count_walls);
  interv := (b_size_x + trunc(b_size_x / count_walls)) * 2;


// обработчик нажатия клавиши
procedure KeyDown(Key: integer);
begin
  if (Key in [32, 38, 87]) then
    k.vel_y := -8;
end;

//конструктор записи блока
function init_block(x, size_x, center: integer): block;
var
  new_block: block;
begin
  new_block.x := x; 
  new_block.size_x := size_x;
  new_block.center := center;
  init_block := new_block;
end;

procedure game_over;
begin
  ClearWindow;
  SetBrushColor(clWhite);
  SetFontSize(20);
  DrawTextCentered(0, 0, WindowWidth, WindowHeight, 'GAME OVER');
  redraw;
end;

begin
  // инициализация мячика
  k.vel_x := 0;
  k.vel_y := 0;
  k.rad := 15;
  k.x := trunc(WindowWidth / 4); 
  k.y := trunc(WindowHeight / 2);
  
  //заполнение массива записей блоков
  setlength(block_arr, count_walls);
  for i: integer := 0 to count_walls - 1 do
    block_arr[i] := init_block(WindowWidth + interv * i, b_size_x, trunc(WindowHeight / 2));
  
  lockdrawing;
  SetFontSize(20);
  OnKeyDown := KeyDown;
  while True do
  begin
    //условие конца игры
    if (k.y < 0) or (k.y > WindowHeight) then
    begin
      game_over;
      break;
    end;
    
    ClearWindow;
    
    // отрисовка мячика
    brush.Color := clYellow;
    DrawCircle(k.x, k.y, k.rad);
    FillCircle(k.x, k.y, k.rad);
    brush.Color := clBlack;
    FillPie(k.x, k.y, k.rad, -15, -50);
    DrawCircle(k.x + 8, k.y - 3, 3);
    PutPixel(k.x + 9, k.y - 3, clBlack);
    
    // ускорение свободного падения
    k.y += k.vel_y;
    k.vel_y += accel;
    
    // отрисовка препятствия/препятствий
    brush.Color := clBrown;
    for i: integer := 0 to count_walls - 1 do
    begin
      block_arr[i].x -= game_speed;
      //условия конца игры
      if (k.x >= block_arr[i].x) and (k.x <= block_arr[i].x + block_arr[i].size_x) and ((k.y >= block_arr[i].center + 50) or (k.y <= block_arr[i].center - 50)) then
      begin
        game_over;
        exit;
      end;
      FillRect(block_arr[i].x, 0, block_arr[i].x + block_arr[i].size_x, block_arr[i].center - 50);
      FillRect(block_arr[i].x, block_arr[i].center + 50, block_arr[i].x + block_arr[i].size_x, WindowHeight);
      //респаун блоков
      if (block_arr[i].x + b_size_x) < 0 then
      begin
        block_arr[i].x := WindowWidth + interv * trunc(count_walls / 2);
        block_arr[i].center := trunc(WindowHeight / 2) + (random(rand_range) - trunc(rand_range / 2)) mod trunc(WindowHeight / 2);
      end;
    end;
    
    // отрисовка счёта
    brush.Color := ARGB(1, 0, 0, 0);
    TextOut(10, 10, 'Score: ' + score);
    
    redraw;
    sleep(20);
    score += 1;//увеличение счёта
    if (score mod difficulty = 0) then
      rand_range += 5;//усложнение игры каждые difficulty очков счёта
  end;
end.