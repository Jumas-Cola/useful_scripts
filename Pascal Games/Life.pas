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
  n = 30;

var
  start_x := 0;
  start_y := 0;
  side_len := 20;
  r := new RectangleStamp(start_x, start_y, side_len, side_len);
  f := new Field(n, n);
  t_f := new Field(n, n);

function neibours_count(i, j, n: integer): integer;
var
  count := 0;
begin
  if (i - 1 >= 0) and (j - 1 >= 0) then
    if t_f.field[i - 1][j - 1] = 1 then
      count += 1;
  if (i - 1 >= 0) then
    if t_f.field[i - 1][j] = 1 then
      count += 1;
  if (i - 1 >= 0) and (j + 1 < n) then
    if t_f.field[i - 1][j + 1] = 1 then
      count += 1;
  if (j - 1 >= 0) then
    if t_f.field[i][j - 1] = 1 then
      count += 1;
  if (j + 1 < n) then
    if t_f.field[i][j + 1] = 1 then
      count += 1;
  if (j - 1 >= 0) and (i + 1 < n) then
    if t_f.field[i + 1][j - 1] = 1 then
      count += 1;
  if (i + 1 < n) then
    if t_f.field[i + 1][j] = 1 then
      count += 1;
  if (i + 1 < n) and (j + 1 < n) then
    if t_f.field[i + 1][j + 1] = 1 then
      count += 1;
  neibours_count := count;
end;

begin
  randomize;
  lockdrawing;
  SetWindowSize((side_len - 1) * n, (side_len - 1) * n);
  for i: integer := 0 to n - 1 do
    for j: integer := 0 to n - 1 do
      f.field[i][j] := random(2);
  while true do
  begin
    for i: integer := 1 to n - 1 do
      for j: integer := 1 to n - 1 do
        t_f.field[i][j] := f.field[i][j];
    for i: integer := 0 to n - 1 do
      for j: integer := 0 to n - 1 do
      begin
          {Существо с двумя или тремя соседями выживает в следующем поколении, иначе погибает от одиночества или перенаселённости.
           В пустой клетке с тремя соседями в следующем поколении рождается существо}
        if (t_f.field[i][j] = 1) then
          if ((neibours_count(i, j, n) = 2) or (neibours_count(i, j, n) = 3)) then
            f.field[i][j] := 1
          else
            f.field[i][j] := 0;
        if (t_f.field[i][j] = 0) then
          if (neibours_count(i, j, n) = 3) then
            f.field[i][j] := 1
          else
            f.field[i][j] := 0;
      end;
    f.DrawField(r);
    redraw;
    sleep(100);
  end;
end.