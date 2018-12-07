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
accel:=1;
score:=0;
game_speed:=5;
difficulty:=500;
count_walls:=8;
rand_range:=20;
block_arr:array of block;
b_size_x:=trunc(WindowWidth/count_walls);
b_size_y:=180;
interv:=b_size_x+trunc(b_size_x/count_walls);


// обработчик нажатия клавиши
procedure KeyDown(Key: integer);
begin 
  if (Key in [32,38,87]) then
    k.vel_y := -8;
end;

//конструктор записи блока
function student_block(x,y,size_x,size_y:integer):block;
var new_block : block;
begin
  new_block.x := x; 
  new_block.y := y;
  new_block.size_x := size_x;
  new_block.size_y := size_y;
  student_block := new_block;
end;

begin
// инициализация мячика
k.vel_x := 0;
k.vel_y := 0;
k.rad := 15;
k.x := trunc(WindowWidth/4); 
k.y := trunc(WindowHeight/2) ;

//заполнение массива записей блоков
setlength(block_arr, count_walls);
for i:integer:=0 to count_walls-1 do
  if ((i mod 2) <> 0)then
    block_arr[i]:=student_block(WindowWidth+interv*i, 0, b_size_x, b_size_y)
  else
    block_arr[i]:=student_block(WindowWidth+interv*i, WindowHeight-b_size_y, b_size_x, b_size_y);

lockdrawing;
SetFontSize(20);
OnKeyDown := KeyDown;
while True do
  begin    
    //условие конца игры
    if (k.y<0) or (k.y>WindowHeight) then
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
    for i:integer:=0 to count_walls-1 do
      begin
        block_arr[i].x-=game_speed;
        //условия конца игры
        if (k.x >= block_arr[i].x) and (k.x <= block_arr[i].x+block_arr[i].size_x) and (k.y >= block_arr[i].y) and (k.y <= block_arr[i].y+block_arr[i].size_y) then
          exit;
        FillRoundRect(block_arr[i].x, block_arr[i].y, block_arr[i].x+block_arr[i].size_x, block_arr[i].y+block_arr[i].size_y, 10, 50);
        //респаун блоков
        if (block_arr[i].x+b_size_x)<0 then
          begin
            block_arr[i].x:=WindowWidth;
            block_arr[i].size_y+=random(rand_range)-trunc(rand_range/2);
            if ((i mod 2) = 0) then
              block_arr[i].y:=WindowHeight-block_arr[i].size_y;
          end;
      end;
    
    // отрисовка счёта
    brush.Color := ARGB(1,0,0,0);
    TextOut(10,10,'Score: '+score);
      
    sleep(20);
    redraw;
    score+=1;//увеличение счёта
    if (score mod difficulty = 0) then
      rand_range+=5;//усложнение игры каждые difficulty очков счёта
  end;
end.