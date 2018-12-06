uses graphABC;

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
dis:=0;
game_speed:=5;
difficulty:=500;
rand_val:integer;
resp_dist:=-50;
floor_height:=100;


// обработчик нажатия клавиши
procedure KeyDown(Key: integer);
begin 
  if (Key in [32,38,87]) and (k.y=(WindowHeight-floor_height-k.rad)) then
    k.vel_y := -15;
end;

begin
// инициализация мячика
k.vel_x := 0;
k.vel_y := 0;
k.rad := 15;
k.x := trunc(WindowWidth/4); 
k.y := WindowHeight-floor_height-k.rad;

// инициализация препятствия
b.size_x := 50;
b.size_y := 50;
b.x := WindowWidth-b.size_x; 
b.y := WindowHeight-floor_height-b.size_y;

lockdrawing;
SetFontSize(20);
OnKeyDown := KeyDown;
while True do
  begin    
    //условия конца игры
    if (k.x in [b.x..b.x+b.size_x]) and (k.y in [b.y..b.y+b.size_y]) then
        break;
    if (k.x in [b.x+200..b.x+b.size_x+200]) and (k.y in [b.y..b.y+b.size_y]) and (rand_val>4) then
        break;
    if (k.x in [b.x+400..b.x+b.size_x+400]) and (k.y in [b.y..b.y+b.size_y]) and (rand_val>=7) then
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
    
    k.y+=k.vel_y;
    k.vel_y+=accel;
    if (k.y=(WindowHeight-floor_height-k.rad)) then
      k.vel_y := 0;
    
    // отрисовка счёта
    brush.Color := clWhite;
    TextOut(10,10,'Score: '+dis);
    
    // отрисовка препятствия/препятствий
    brush.Color := clBrown;
    FillRoundRect(b.x, b.y, b.x+b.size_x, b.y+b.size_y, 10, 50);
    resp_dist:=-50;
    if rand_val=0 then
      rand_val:=random(10);//случайное число, определяющее количество препятствий
    if (rand_val>4) and (rand_val<7) then//если больше 4, но меньше 7 - то два препятствия
      begin
        FillRoundRect(b.x+200, b.y, b.x+b.size_x+200, b.y+b.size_y, 10, 50);
        resp_dist:=-250;
      end
    else if rand_val>=7 then//если больше или равно 7 - то три препятствия
      begin
        FillRoundRect(b.x+200, b.y, b.x+b.size_x+200, b.y+b.size_y, 10, 50);
        FillRoundRect(b.x+400, b.y, b.x+b.size_x+400, b.y+b.size_y, 10, 50);
        resp_dist:=-450;
      end;
      
    //отрисовка земли
    brush.Color := clGreen;
    FillRectangle(0, WindowHeight-floor_height, WindowWidth, WindowHeight);
    
    b.x-=game_speed;//обновление координаты препятствий в зависимости от скорости игры
    
    //респаун препятствий в конце экрана
    if (b.x<resp_dist) then
      begin
        b.x:=random(150)+WindowWidth+10;
        rand_val:=0;
      end;
      
    sleep(20);
    redraw;
    dis+=1;//увеличение счёта
    if (dis mod difficulty = 0) then
      game_speed+=1;//ускорение игры каждые difficulty очков счёта
  end;
end.