uses graphABC;
uses ABCObjects;

var
    kolobok_rad := 15;
    kolobok := new CircleABC(trunc(WindowWidth / 4), trunc(WindowHeight / 2), kolobok_rad);
    top_blk_arr: array of RectangleABC;
    btm_blk_arr: array of RectangleABC;
    center_arr: array of integer;
    accel := 1;
    vel_y := 0;
    blk_vel := 3;
    block_count := 4;
    b_size_x := 80;
    interv := 150;
    k: integer;
    score := 0;
    txt_score := new TextABC(10,10,20,'Score: '+score);
    difficulty := 100;
    rand_range := 40;

// обработчик нажатия клавиши
procedure KeyDown(Key: integer);
begin
    if (Key in [32, 38, 87]) then
        vel_y := -8;
end;

procedure game_over;
begin
    SetFontSize(20);
    DrawTextCentered(0, 0, WindowWidth, WindowHeight, 'GAME OVER');
    DrawTextCentered(0, 0, WindowWidth, trunc(WindowHeight*1.2), 'Score: '+score);
end;

begin
    kolobok.Color := clYellow;
    setlength(top_blk_arr, block_count);
    setlength(btm_blk_arr, block_count);
    setlength(center_arr, block_count);
    for i: integer := 0 to block_count - 1 do
    begin
        center_arr[i] := trunc(WindowHeight / 2);
        top_blk_arr[i] := new RectangleABC(WindowWidth + (b_size_x + interv) * i, 0, b_size_x, center_arr[i] - 50);
        btm_blk_arr[i] := new RectangleABC(WindowWidth + (b_size_x + interv) * i, center_arr[i] + 50, b_size_x, WindowHeight);
        top_blk_arr[i].Color := clLightGreen;
        btm_blk_arr[i].Color := clLightGreen;
    end;
    
    OnKeyDown := KeyDown;
    while true do
    begin
        if (kolobok.Position.Y + 2 * kolobok_rad > WindowHeight) or (kolobok.Position.Y < 0) then
        begin
            game_over;
            exit;
        end;
        kolobok.MoveOn(0, vel_y);
        vel_y += accel;
        
        for i: integer := 0 to block_count - 1 do
        begin
            top_blk_arr[i].MoveOn(-blk_vel, 0);
            btm_blk_arr[i].MoveOn(-blk_vel, 0);
            if top_blk_arr[i].Position.X + b_size_x < 0 then
            begin
                if i > 0 then k := i - 1 else k := block_count - 1;
                top_blk_arr[i].MoveTo(top_blk_arr[k].Position.X + b_size_x + interv, 0);
                center_arr[i] := trunc(WindowHeight / 2) + (random(rand_range) - trunc(rand_range / 2)) mod trunc(WindowHeight / 2);
                top_blk_arr[i].Height := center_arr[i] - 50;
                btm_blk_arr[i].MoveTo(btm_blk_arr[k].Position.X + b_size_x + interv, center_arr[i] + 50);
            end;
            if kolobok.Intersect(top_blk_arr[i]) or kolobok.Intersect(btm_blk_arr[i]) then
            begin
                game_over;
                exit;
            end;
        end;
        
        score += 1;
        txt_score.Text:='Score: '+score;
        txt_score.ToFront;       
        sleep(15);
        if (score mod difficulty = 0) then
            rand_range += 5;
    end;
end.