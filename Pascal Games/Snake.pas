uses graphABC;

type
  RectangleStamp = class
    x, y, w, h: integer;
    clr: Color;
    constructor(xx, yy, width, height: integer; colored: Color := clWhite);
    begin
      x := xx; y := yy;
      w := width; h := height;
      clr := colored;
    end;
    //отрисовка прямоугольника
    procedure Stamp;
    begin
      SetBrushColor(clr); 
      FillRect(x, y, x + w, y + h);
      SetBrushColor(clBlack);
      DrawRectangle(x, y, x + w, y + h);
    end;
  end;

type
  Field = class
    n, m: integer;
    field: array of array of integer;
    field_row: array of integer;
    constructor(n_x, m_y: integer);
    begin
      n := n_x; m := m_y;
      SetLength(field, n);
      SetLength(field_row, m);
      for i: integer := 0 to n - 1 do
      begin
        field[i] := field_row;
        SetLength(field_row, 0);
        SetLength(field_row, m);
      end;
    end;
    //отрисовка поля
    procedure DrawField(r: RectangleStamp);
    var
      start_x := r.x;
      start_y := r.y;
    begin
      ClearWindow;
      for i: integer := 0 to field.Length - 1 do
      begin
        for j: integer := 0 to field[0].Length - 1 do
        begin
          if field[i][j] = 1 then
            r.clr := clLightGreen
          else if field[i][j] = 2 then
            r.clr := clLightPink
          else
            r.clr := clWhite;
          r.Stamp;
          r.x += r.h - 1;
        end;
        r.y += r.h - 1;
        r.x := start_x;
      end;
      r.x := start_x;
      r.y := start_y;
    end;
  end;

type
  square = record
    x: integer;
    y: integer;
    dir: char;
  end;

const
  n = 20;

var
  start_x := 0;
  start_y := 0;
  side_len := 30;
  r := new RectangleStamp(start_x, start_y, side_len, side_len);
  f := new Field(n, n);
  sq: square;
  sq_arr: array of square;
  x_arr: array of integer;
  y_arr: array of integer;
  apple_x := -1;
  apple_y := -1;
  succes_apple_coords: boolean;
  prev_dir: char;

// обработчик нажатия клавиши
procedure KeyDown(Key: integer);
begin
  if (Key = 38) and (prev_dir <> 'b') then
    sq_arr[0].dir := 't'
  else if (Key = 40) and (prev_dir <> 't') then
    sq_arr[0].dir := 'b'
  else if (Key = 37) and (prev_dir <> '0') and (prev_dir <> 'r') then
    sq_arr[0].dir := 'l'
  else if (Key = 39) and (prev_dir <> 'l') then
    sq_arr[0].dir := 'r';
end;

function square_init(x, y: integer; dir: char := '0'): square;
var
  new_square: square;
begin
  new_square.x := x;
  new_square.y := y;
  new_square.dir := dir;
  square_init := new_square;
end;

begin
  // инициализация змейки
  var snake_len := 3;
  SetLength(x_arr, snake_len);
  SetLength(y_arr, snake_len);
  SetLength(sq_arr, snake_len);
  sq_arr[0] := square_init(trunc(n / 2), trunc(n / 2));
  
  //создание массива записей
  for i: integer := 1 to snake_len - 1 do
    sq_arr[i] := square_init(sq_arr[i - 1].x, sq_arr[i - 1].y - 1);
  
  SetWindowSize((side_len - 1) * n, (side_len - 1) * n);
  lockdrawing;
  OnKeyDown := KeyDown;
  
  while true do
  begin
    SetLength(x_arr, snake_len);
    SetLength(y_arr, snake_len);
    SetLength(sq_arr, snake_len);
     //сохранение координат в промежуточный массив
    for i: integer := 0 to snake_len - 1 do
      x_arr[i] := sq_arr[i].x;
    for i: integer := 0 to snake_len - 1 do
      y_arr[i] := sq_arr[i].y;
    
     //обновление координат(ползание змейки)
    if sq_arr[0].dir in 'tblr' then
      for i: integer := 1 to snake_len - 1 do
      begin
        sq_arr[i].x := x_arr[i - 1];
        sq_arr[i].y := y_arr[i - 1];
      end;
    
     //поворот головы в завистимости от направления
    if (sq_arr[0].dir = 't') then
      sq_arr[0].x -= 1
    else if (sq_arr[0].dir = 'b') then
      sq_arr[0].x += 1
    else if (sq_arr[0].dir = 'l') then
      sq_arr[0].y -= 1
    else if (sq_arr[0].dir = 'r') then
      sq_arr[0].y += 1;
    
     //выход с обратной стороны поля,при пересечении границы
    for i: integer := 0 to snake_len - 1 do
    begin
      if sq_arr[i].x > n - 1 then
        sq_arr[i].x := 0
      else if sq_arr[i].x < 0 then
        sq_arr[i].x := n - 1;
      if sq_arr[i].y > n - 1 then
        sq_arr[i].y := 0
      else if sq_arr[i].y < 0 then
        sq_arr[i].y := n - 1;
    end;
    
     //очистка поля
    for i: integer := 0 to n - 1 do
      for j: integer := 0 to n - 1 do
        f.field[i][j] := 0;
    
     //установка закрашенных пикселей
    for i: integer := 0 to snake_len - 1 do
      f.field[sq_arr[i].x][sq_arr[i].y] := 1;
    
     //условие конца игры
    for i: integer := 1 to snake_len - 1 do
      if (sq_arr[0].x = sq_arr[i].x) and (sq_arr[0].y = sq_arr[i].y) then
      begin
        SetBrushColor(clWhite);
        SetFontSize(20);
        DrawTextCentered(0, 0, WindowWidth, WindowHeight, 'GAME OVER');
        redraw;
        exit;
      end;
    
     //сохранение координат в промежуточный массив
    for i: integer := 0 to snake_len - 1 do
      x_arr[i] := sq_arr[i].x;
    for i: integer := 0 to snake_len - 1 do
      y_arr[i] := sq_arr[i].y;
    
     //установка яблока
    if ((apple_x = -1) and (apple_y = -1)) or ((sq_arr[0].x = apple_x) and (sq_arr[0].y = apple_y)) then
    begin
      if (sq_arr[0].x = apple_x) and (sq_arr[0].y = apple_y) then
        snake_len += 1;
      succes_apple_coords := false;
      while not succes_apple_coords do
      begin
        apple_x := random(n);
        apple_y := random(n);
        succes_apple_coords := true;
        for i: integer := 0 to x_arr.length - 1 do
          if (apple_x = x_arr[i]) and (apple_y = y_arr[i]) then
          begin
            succes_apple_coords := false;
            break;
          end;
      end;
    end;
    f.field[apple_x][apple_y] := 2;
    
    //переменная для запрета поворота "внутрь себя"
    prev_dir := sq_arr[0].dir;
    
    //условие победы
    if snake_len = n * n then
    begin
      SetBrushColor(clWhite);
      SetFontSize(20);
      DrawTextCentered(0, 0, WindowWidth, WindowHeight, 'YOU WIN!');
      redraw;
      exit;
    end;
    
    f.DrawField(r);
    redraw;
    sleep(300);
  end;
end. 