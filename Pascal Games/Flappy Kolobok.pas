uses graphABC;
uses Arrays;

type circle=record
  x: integer;
  y: integer;
  rad: integer;
  vel_x: integer;
  vel_y: integer;
end;

type block=record
  x: integer;
  y: integer;
  size_x: integer;
  size_y: integer;
end;

var
k: circle; 
b: block;
accel:=1;
score:=0;
game_speed:=5;
difficulty:=500;
interv:=160;
count_walls:=11;
resp_dist:integer;
rand_range:=20;
rand_arr:=CreateRandomIntegerArray(count_walls+1,-rand_range,rand_range);


// обработчик нажатия клавиши
procedure KeyDown(Key: integer);
begin 
  if (Key in [32,38,87]) then
    k.vel_y := -8;
end;

begin
// инициализация мячика
k.vel_x := 0;
k.vel_y := 0;
k.rad := 15;
k.x := trunc(WindowWidth/4); 
k.y := trunc(WindowHeight/2) ;

// инициализация препятствия
b.size_x := 110;
b.size_y := 200;
b.x := WindowWidth-b.size_x; 
b.y := WindowHeight-b.size_y; 

lockdrawing;
SetFontSize(20);
OnKeyDown := KeyDown;
resp_dist:=-interv*count_walls-b.size_x;
while True do
  begin    
    //условия конца игры
    if (k.y<0) or (k.y>WindowHeight) then
        break;
    
    if (k.x in [b.x..b.x+b.size_x]) and (k.y in [b.y+rand_arr[0]..b.y+b.size_y]) then
        break;
    if (k.x in [b.x+interv..b.x+b.size_x+interv]) and (k.y in [0..b.size_y+rand_arr[1]]) then
        break;
    if (k.x in [b.x+interv*2..b.x+b.size_x+interv*2]) and (k.y in [b.y+rand_arr[2]..b.y+b.size_y]) then
        break;
    if (k.x in [b.x+interv*3..b.x+b.size_x+interv*3]) and (k.y in [0..b.size_y+rand_arr[3]]) then
        break;
    if (k.x in [b.x+interv*4..b.x+b.size_x+interv*4]) and (k.y in [b.y+rand_arr[4]..b.y+b.size_y]) then
        break;
    if (k.x in [b.x+interv*5..b.x+b.size_x+interv*5]) and (k.y in [0..b.size_y+rand_arr[5]]) then
        break;
    if (k.x in [b.x+interv*6..b.x+b.size_x+interv*6]) and (k.y in [b.y+rand_arr[6]..b.y+b.size_y]) then
        break;
    if (k.x in [b.x+interv*7..b.x+b.size_x+interv*7]) and (k.y in [0..b.size_y+rand_arr[7]]) then
        break;
    if (k.x in [b.x+interv*8..b.x+b.size_x+interv*8]) and (k.y in [b.y+rand_arr[8]..b.y+b.size_y]) then
        break;
    if (k.x in [b.x+interv*9..b.x+b.size_x+interv*9]) and (k.y in [0..b.size_y+rand_arr[9]]) then
        break;
    if (k.x in [b.x+interv*10..b.x+b.size_x+interv*10]) and (k.y in [b.y+rand_arr[10]..b.y+b.size_y]) then
        break;
    if (k.x in [b.x+interv*11..b.x+b.size_x+interv*11]) and (k.y in [0..b.size_y+rand_arr[11]]) then
        break;
    
           
    ClearWindow;
    
    // отрисовка мячика
    brush.Color := clYellow;
    DrawCircle(k.x,k.y,k.rad);
    FillCircle(k.x,k.y,k.rad);
    brush.Color := clBlack;
    FillPie(k.x, k.y, k.rad, -15, -50);
    DrawCircle(k.x+8,k.y-3,3);
    PutPixel(k.x+9,k.y-3,clBlack);
    
    // ускорение свободного падения
    k.y+=k.vel_y;
    k.vel_y+=accel;
    
    // отрисовка препятствия/препятствий
    brush.Color := clBrown;
    for i:integer:=0 to count_walls do
      if ((i mod 2) <> 0) and (i<>0) then
        FillRoundRect(b.x+interv*i, 0, b.x+b.size_x+interv*i, b.size_y+rand_arr[i], 10, 50)
      else
        FillRoundRect(b.x+interv*i, b.y+rand_arr[i], b.x+b.size_x+interv*i, b.y+b.size_y, 10, 50);
    
    // отрисовка счёта
    brush.Color := ARGB(1,0,0,0);
    TextOut(10,10,'Score: '+score);
    
    b.x-=game_speed;//обновление координаты препятствий в зависимости от скорости игры
    
    //респаун препятствий в конце экрана
    if (b.x<resp_dist) then
      begin
        b.x:=WindowWidth;
        rand_arr:=CreateRandomIntegerArray(count_walls+1,-rand_range,rand_range);
      end;
      
    sleep(20);
    redraw;
    score+=1;//увеличение счёта
    if (score mod difficulty = 0) then
      rand_range+=5;//усложнение игры каждые difficulty очков счёта
  end;
end.