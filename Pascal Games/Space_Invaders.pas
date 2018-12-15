uses graphABC;
uses ABCObjects;

var
    ship_rad := 10;
    inv_count := 11;
    ship := new RegularPolygonABC(trunc(WindowWidth / 2), WindowHeight - 20, ship_rad, 3);
    invaders_arr_0: array of RectangleABC;
    invaders_arr_1: array of CircleABC;
    invaders_arr_2: array of RegularPolygonABC;
    invaders_arr_3: array of RegularPolygonABC;
    invaders_arr_4: array of StarABC;
    vel_x := 8;
    bullet := new CircleABC(-6, -6, 3, clGreen);
    inv_bullet := new CircleABC(WindowHeight + 6, WindowHeight + 6, 3, clRed);
    block_arr_0: array of RectangleABC;
    block_arr_1: array of RectangleABC;
    block_arr_2: array of RectangleABC;
    block_arr_3: array of RectangleABC;
    inv_dir := 1;
    cycles := 0;
    lives := 3;
    score := 0;
    txt_lives := new TextABC(10, 10, 20, '♥ ' + lives);
    rand_num: integer;
    rand_arr: integer;

// обработчик нажатия клавиши
procedure KeyDown(Key: integer);
begin
    case Key of 
        37: if ship.Center.X > 40 then ship.MoveOn(-vel_x, 0);
        39: if ship.Center.X < WindowWidth - 40 then ship.MoveOn(vel_x, 0);
        32: if (bullet.Center.Y < 0) then bullet.MoveTo(ship.Center.X - 4, ship.Center.Y - 3);
    end;
end;

procedure game_over;
begin
    SetFontSize(20);
    DrawTextCentered(0, 0, WindowWidth, WindowHeight, 'GAME OVER');
    DrawTextCentered(0, 0, WindowWidth, trunc(WindowHeight * 1.2), 'Score: ' + score);
end;

procedure win;
begin
    SetFontSize(20);
    DrawTextCentered(0, 0, WindowWidth, WindowHeight, 'YOU WIN!');
    DrawTextCentered(0, 0, WindowWidth, trunc(WindowHeight * 1.2), 'Score: ' + score);
end;

procedure invaders_bullet;
begin
    rand_arr := random(5);
    if rand_arr = 0 then
    begin
        rand_num := random(inv_count - 1);
        if invaders_arr_0[rand_num].Color <> clWhite then
            inv_bullet.MoveTo(invaders_arr_0[rand_num].Center.X, invaders_arr_0[rand_num].Center.Y);
    end
    else if rand_arr = 1 then
    begin
        rand_num := random(inv_count - 1);
        if invaders_arr_1[rand_num].Color <> clWhite then
            inv_bullet.MoveTo(invaders_arr_1[rand_num].Center.X, invaders_arr_1[rand_num].Center.Y);
    end
    else if rand_arr = 2 then
    begin
        rand_num := random(inv_count - 1);
        if invaders_arr_2[rand_num].Color <> clWhite then
            inv_bullet.MoveTo(invaders_arr_2[rand_num].Center.X, invaders_arr_2[rand_num].Center.Y);
    end
    else if rand_arr = 3 then
    begin
        rand_num := random(inv_count - 1);
        if invaders_arr_3[rand_num].Color <> clWhite then
            inv_bullet.MoveTo(invaders_arr_3[rand_num].Center.X, invaders_arr_3[rand_num].Center.Y);
    end
    else if rand_arr = 4 then
    begin
        rand_num := random(inv_count - 1);
        if invaders_arr_4[rand_num].Color <> clWhite then
            inv_bullet.MoveTo(invaders_arr_4[rand_num].Center.X, invaders_arr_4[rand_num].Center.Y);
    end;
end;

procedure check_kill_invaders;
begin
    for i: integer := 0 to inv_count - 1 do
    begin
        if bullet.Intersect(invaders_arr_0[i]) and (invaders_arr_0[i].Color <> clWhite) then
        begin
            invaders_arr_0[i].Color := clWhite;
            invaders_arr_0[i].Destroy;
            score += 500;
            bullet.MoveTo(-6, -6);
        end;
        if bullet.Intersect(invaders_arr_1[i]) and (invaders_arr_1[i].Color <> clWhite) then
        begin
            invaders_arr_1[i].Color := clWhite;
            invaders_arr_1[i].Destroy;
            score += 400;
            bullet.MoveTo(-6, -6);
        end;
        if bullet.Intersect(invaders_arr_2[i]) and (invaders_arr_2[i].Color <> clWhite) then
        begin
            invaders_arr_2[i].Color := clWhite;
            invaders_arr_2[i].Destroy;
            score += 300;
            bullet.MoveTo(-6, -6);
        end;
        if bullet.Intersect(invaders_arr_3[i]) and (invaders_arr_3[i].Color <> clWhite) then
        begin
            invaders_arr_3[i].Color := clWhite;
            invaders_arr_3[i].Destroy;
            score += 200;
            bullet.MoveTo(-6, -6);
        end;
        if bullet.Intersect(invaders_arr_4[i]) and (invaders_arr_4[i].Color <> clWhite) then
        begin
            invaders_arr_4[i].Color := clWhite;
            invaders_arr_4[i].Destroy;
            score += 100;
            bullet.MoveTo(-6, -6);
        end;
    end;
end;

procedure move_invaders_y(n: integer);
begin
    for i: integer := 0 to inv_count - 1 do
    begin
        invaders_arr_0[i].MoveOn(n, 0);
        invaders_arr_1[i].MoveOn(n, 0);
        invaders_arr_2[i].MoveOn(n, 0);
        invaders_arr_3[i].MoveOn(n, 0);
        invaders_arr_4[i].MoveOn(n, 0);
    end
end;

procedure move_invaders_x(n: integer);
begin
    for i: integer := 0 to inv_count - 1 do
    begin
        invaders_arr_0[i].MoveOn(0, n);
        invaders_arr_1[i].MoveOn(0, n);
        invaders_arr_2[i].MoveOn(0, n);
        invaders_arr_3[i].MoveOn(0, n);
        invaders_arr_4[i].MoveOn(0, n);
    end;
end;

function check_lose: boolean;
var
    lose := false;
begin
    for i: integer := 0 to inv_count - 1 do
    begin
        if (invaders_arr_4[i].Center.Y > WindowHeight - 100) and (invaders_arr_4[i].Color <> clWhite) then
        begin
            lose := true;
            break;
        end
        else if (invaders_arr_3[i].Center.Y > WindowHeight - 100) and (invaders_arr_3[i].Color <> clWhite) then
        begin
            lose := true;
            break;
        end
        else if (invaders_arr_2[i].Center.Y > WindowHeight - 100) and (invaders_arr_2[i].Color <> clWhite) then
        begin
            lose := true;
            break;
        end
        else if (invaders_arr_1[i].Center.Y > WindowHeight - 100) and (invaders_arr_1[i].Color <> clWhite) then
        begin
            lose := true;
            break;
        end
        else if (invaders_arr_0[i].Center.Y > WindowHeight - 100) and (invaders_arr_0[i].Color <> clWhite) then
        begin
            lose := true;
            break;
        end
    end;
    check_lose := lose;
end;

function check_win: boolean;
var
    is_win := true;
begin
    for i: integer := 0 to inv_count - 1 do
    begin
        if invaders_arr_0[i].Color <> clWhite then
        begin
            is_win := false;
            break;
        end
        else if invaders_arr_1[i].Color <> clWhite then
        begin
            is_win := false;
            break;
        end
        else if invaders_arr_2[i].Color <> clWhite then
        begin
            is_win := false;
            break;
        end
        else if invaders_arr_3[i].Color <> clWhite then
        begin
            is_win := false;
            break;
        end
        else if invaders_arr_4[i].Color <> clWhite then
        begin
            is_win := false;
            break;
        end
    end;
    check_win := is_win;
end;

procedure check_block_destroy;
begin
    for i: integer := 0 to 11 do
    begin
        if bullet.Intersect(block_arr_0[i]) and (block_arr_0[i].Color <> clWhite) then
        begin
            block_arr_0[i].Color := clWhite;
            block_arr_0[i].Destroy;
            bullet.MoveTo(-6, -6);
        end
        else if bullet.Intersect(block_arr_1[i]) and (block_arr_1[i].Color <> clWhite) then
        begin
            block_arr_1[i].Color := clWhite;
            block_arr_1[i].Destroy;
            bullet.MoveTo(-6, -6);
        end
        else if bullet.Intersect(block_arr_2[i]) and (block_arr_2[i].Color <> clWhite) then
        begin
            block_arr_2[i].Color := clWhite;
            block_arr_2[i].Destroy;
            bullet.MoveTo(-6, -6);
        end
        else if bullet.Intersect(block_arr_3[i]) and (block_arr_3[i].Color <> clWhite) then
        begin
            block_arr_3[i].Color := clWhite;
            block_arr_3[i].Destroy;
            bullet.MoveTo(-6, -6);
        end;
        if inv_bullet.Intersect(block_arr_0[i]) and (block_arr_0[i].Color <> clWhite) then
        begin
            block_arr_0[i].Color := clWhite;
            block_arr_0[i].Destroy;
            inv_bullet.MoveTo(WindowHeight + 6, WindowHeight + 6);
        end
        else if inv_bullet.Intersect(block_arr_1[i]) and (block_arr_1[i].Color <> clWhite) then
        begin
            block_arr_1[i].Color := clWhite;
            block_arr_1[i].Destroy;
            inv_bullet.MoveTo(WindowHeight + 6, WindowHeight + 6);
        end
        else if inv_bullet.Intersect(block_arr_2[i]) and (block_arr_2[i].Color <> clWhite) then
        begin
            block_arr_2[i].Color := clWhite;
            block_arr_2[i].Destroy;
            inv_bullet.MoveTo(WindowHeight + 6, WindowHeight + 6);
        end
        else if inv_bullet.Intersect(block_arr_3[i]) and (block_arr_3[i].Color <> clWhite) then
        begin
            block_arr_3[i].Color := clWhite;
            block_arr_3[i].Destroy;
            inv_bullet.MoveTo(WindowHeight + 6, WindowHeight + 6);
        end;
    end;
end;

begin
    SetLength(invaders_arr_0, inv_count);
    SetLength(invaders_arr_1, inv_count);
    SetLength(invaders_arr_2, inv_count);
    SetLength(invaders_arr_3, inv_count);
    SetLength(invaders_arr_4, inv_count);
    SetLength(block_arr_0, 12);
    SetLength(block_arr_1, 12);
    SetLength(block_arr_2, 12);
    SetLength(block_arr_3, 12);
    SetWindowSize(640, 480); 
    SetWindowIsFixedSize(true);
    for i: integer := 0 to 11 do
    begin
        block_arr_0[i] := new RectangleABC(50 + 20 * (i mod 4), WindowHeight - (100 - (i div 4) * 20), 20, 20, clGray);
        block_arr_1[i] := new RectangleABC(200 + 20 * (i mod 4), WindowHeight - (100 - (i div 4) * 20), 20, 20, clGray);
        block_arr_2[i] := new RectangleABC(350 + 20 * (i mod 4), WindowHeight - (100 - (i div 4) * 20), 20, 20, clGray);
        block_arr_3[i] := new RectangleABC(500 + 20 * (i mod 4), WindowHeight - (100 - (i div 4) * 20), 20, 20, clGray);
    end;
    for i: integer := 0 to inv_count - 1 do
    begin
        invaders_arr_0[i] := new RectangleABC(40 + i * 50, 50, 20, 20, clGreen);
        invaders_arr_1[i] := new CircleABC(50 + i * 50, 100, 10, clRed);
        invaders_arr_2[i] := new RegularPolygonABC(50 + i * 50, 150, 10, 5, clYellow);
        invaders_arr_3[i] := new RegularPolygonABC(50 + i * 50, 200, 10, 3, clBlue);
        invaders_arr_4[i] := new StarABC(50 + i * 50, 250, 10, 3, 5, clOrange);
    end;
    ship.Color := clBlack;   
    OnKeyDown := KeyDown;
    while true do
    begin
        if bullet.Center.Y + 3 > 0 then
            bullet.MoveOn(0, -8);
        if inv_bullet.Center.Y - 3 < WindowHeight then
            inv_bullet.MoveOn(0, 8);
        check_kill_invaders;
        if (cycles mod 800 = 0) and (cycles <> 0) then
            move_invaders_x(20);
        if invaders_arr_0[0].Center.X < 40 then
            inv_dir := 1;
        if invaders_arr_0[inv_count - 1].Center.X > WindowWidth - 40 then
            inv_dir := 0;
        if inv_bullet.Center.Y > WindowHeight then
            invaders_bullet;
        if cycles mod 100 = 0 then
            if inv_dir = 1 then
                move_invaders_y(6)
            else
                move_invaders_y(-6);
        check_block_destroy;
        if inv_bullet.Intersect(ship) then
        begin
            lives -= 1;
            inv_bullet.MoveTo(WindowHeight + 6, WindowHeight + 6);
            txt_lives.Text := '♥ ' + lives;
            if lives = 0 then
            begin
                game_over;
                exit;
            end
        end;
        if check_lose then
        begin
            game_over;
            exit;
        end;
        if check_win then
        begin
            win;
            exit;
        end;
        cycles += 1;
        sleep(15);
    end;
end.