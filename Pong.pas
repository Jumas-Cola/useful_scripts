uses graphABC;

type circle=record
  x: integer;
  y: integer;
  rad: integer;
  vel_x: integer;
  vel_y: integer;
end;

type pad=record
  x: integer;
  y: integer;
  size_x: integer;
  size_y: integer;
  vel: integer;
end;

var
rp: pad;
lp: pad;
b: circle;
r_up := false;
r_down := false;
l_up := false;
l_down := false;
l_goals: integer;
r_goals: integer;
start_b_vel_x := 15; // начальная скорость мячика
rand_y := 6; // случайный отскока по оси "y"

// обработчик нажатия клавиши
procedure KeyDown(Key: integer);
begin 
  case Key of 
    38:  r_up := true;//Up
    40:  r_down := true;//Down
    87:  l_up := true;//Up
    83:  l_down := true;//Down
  end;
end;

// обработчик отпускания клавиши
procedure KeyUp(Key: integer);
begin 
  case Key of 
    38:  r_up := false;//Up
    40:  r_down := false;//Down
    87:  l_up := false;//Up
    83:  l_down := false;//Down
  end;
end;

// автоматическая игра левой ракетки
procedure auto_play_l(start_vel:integer);
begin
var lp_y_center := lp.y + trunc(lp.size_y/2);
if b.y <> lp_y_center then
  begin
    if abs(b.y - lp_y_center) <= start_vel then
      lp.vel := sign(b.y - lp_y_center)
    else
      lp.vel := sign(b.y - lp_y_center) * start_vel;
    lp.y += lp.vel;
  end;
end;

// автоматическая игра правой ракетки
procedure auto_play_r(start_vel:integer);
begin
var rp_y_center := rp.y + trunc(rp.size_y/2);
if b.y <> rp_y_center then
  begin
    if abs(b.y - rp_y_center) <= start_vel then
      rp.vel := sign(b.y - rp_y_center)
    else
      rp.vel := sign(b.y - rp_y_center) * start_vel;
    rp.y += rp.vel;
  end;
end;

begin
// инициализация правой ракетки
rp.size_x := 20;
rp.size_y := 150;
rp.x := WindowWidth-rp.size_x; 
rp.y := trunc(WindowHeight/2)-trunc(rp.size_y/2);
rp.vel := 15;

// инициализация левой ракетки
lp.size_x := rp.size_x;
lp.size_y := rp.size_y;
lp.x := 0; 
lp.y := trunc(WindowHeight/2)-trunc(lp.size_y/2);
lp.vel := rp.vel;

// инициализация мячика
b.x := trunc(WindowWidth/2); 
b.y := trunc(WindowHeight/2);
b.vel_x := start_b_vel_x;
b.vel_y := random(rand_y)-trunc(rand_y/2);
b.rad := 15;

OnKeyDown := KeyDown;
OnKeyUp := KeyUp;
lockdrawing;
brush.Color := clBlack;
while True do
  begin
    // респаун мячика
    if (b.x > WindowWidth) then
      begin
        b.x := trunc(WindowWidth/2); 
        b.y := trunc(WindowHeight/2);
        b.vel_x:=start_b_vel_x;
        b.vel_y := random(rand_y)-trunc(rand_y/2);
        l_goals+=1;
      end
    else if (b.x < 0) then
      begin
        b.x := trunc(WindowWidth/2); 
        b.y := trunc(WindowHeight/2);
        b.vel_x:=-start_b_vel_x;
        b.vel_y := random(rand_y)-trunc(rand_y/2);
        r_goals+=1;
      end;
    // отскок от верхней и нижней стенки
    if ((b.y+b.rad)>=WindowHeight) or ((b.y-b.rad)<=0) then
      b.vel_y:=-b.vel_y;
    // отскок от правой ракетки
    if (b.x > (WindowWidth-rp.size_x-b.rad)) and (b.y in [rp.y..rp.y+rp.size_y]) then
      begin
        b.x := WindowWidth-rp.size_x-b.rad;
        b.vel_x:=-b.vel_x;
        b.vel_y+=random(rand_y)-trunc(rand_y/2);
      end;
    // отскок от левой ракетки
    if (b.x < (lp.size_x+b.rad)) and (b.y in [lp.y..lp.y+lp.size_y]) then
      begin
        b.x := lp.size_x+b.rad;
        b.vel_x:=-b.vel_x;
        b.vel_y+=random(rand_y)-trunc(rand_y/2);
      end;
    // ограничение ракеток от выхода за экран
    if rp.y<0 then
      rp.y:=0;
    if rp.y+rp.size_y>WindowHeight then
      rp.y:=WindowHeight-rp.size_y;
    if lp.y<0 then
      lp.y:=0;
    if lp.y+rp.size_y>WindowHeight then
      lp.y:=WindowHeight-rp.size_y;
    
    // обновление координат в зависимости от нажатых клавиш
    if r_up then rp.y := rp.y - rp.vel//Up
    else if r_down then rp.y := rp.y + rp.vel;//Down
    if l_up then lp.y := lp.y - lp.vel//Up
    else if l_down then lp.y := lp.y + lp.vel;//Down
    
    auto_play_l(4);// автоматическая игра левой ракетки
    //auto_play_r(8);// автоматическая игра правой ракетки
    
    ClearWindow;
    rp.x := WindowWidth-rp.size_x;
    lp.x := 0;
    SetFontSize(25);
    // отрисовка счёта
    DrawTextCentered(0, 0, WindowWidth, trunc(WindowHeight/3),l_goals+'     '+r_goals);
    // отрисовка разметки поля
    Line(trunc(WindowWidth/2), 0, trunc(WindowWidth/2), WindowHeight);
    DrawCircle(trunc(WindowWidth/2), trunc(WindowHeight/2), trunc(WindowWidth/5));
    // отрисовка правой ракетки
    FillRectangle(rp.x, rp.y, rp.x+rp.size_x, rp.y+rp.size_y);
    // отрисовка левой ракетки
    FillRectangle(lp.x, lp.y, lp.x+lp.size_x, lp.y+lp.size_y);
    // отрисовка мячика
    FillCircle(b.x,b.y,b.rad);
    b.x+=b.vel_x;
    b.y+=b.vel_y;
    sleep(20);
    redraw;
  end;
end. 