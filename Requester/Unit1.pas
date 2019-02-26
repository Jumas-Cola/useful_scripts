unit Unit1;

interface

uses
  System.SysUtils, System.Types, System.UITypes, System.Classes, System.Variants,
  FMX.Types, FMX.Controls, FMX.Forms, FMX.Graphics, FMX.Dialogs,
  FMX.Controls.Presentation, FMX.StdCtrls, FMX.Edit, FMX.ListBox,
  Data.DB, Data.Win.ADODB, IdHTTP;

type
  TForm1 = class(TForm)
    Button1: TButton;
    ADOQuery1: TADOQuery;
    Label2: TLabel;
    Edit2: TEdit;
    ComboBox1: TComboBox;
    Button2: TButton;
    Button3: TButton;
    Label1: TLabel;
    ADOConnection1: TADOConnection;
    procedure FormCreate(Sender: TObject);
    procedure Button2Click(Sender: TObject);
    procedure Button3Click(Sender: TObject);
    procedure Button1Click(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Form1: TForm1;

implementation

{$R *.fmx}

function GetPage(aURL: string): string;
var
  Response: TStringStream;
  HTTP: TIdHTTP;
begin
  Result := '';
  Response := TStringStream.Create('');
  try
    HTTP := TIdHTTP.Create(nil);
    try
      HTTP.Get(aURL, Response);
      if HTTP.ResponseCode = 200 then begin
        Result := Response.DataString;
      end else begin
        // Nothing returned or error
      end;
    finally
      HTTP.Free;
    end;
  finally
    Response.Free;
  end;
end;

procedure TForm1.Button1Click(Sender: TObject);
var page: string;
begin
try
  page := GetPage(Combobox1.Items[Combobox1.ItemIndex]);
  ShowMessage('Запрос успешно выполнен');
except
  ShowMessage('Выполнить запрос не удалось');
end;
end;

procedure TForm1.Button2Click(Sender: TObject);
begin
ADOQuery1.Open;
while ADOQuery1.Locate('URL', Combobox1.Items[Combobox1.ItemIndex], []) do
  ADOQuery1.Delete;
ComboBox1.Items.Clear;
ADOQuery1.First;
while not ADOQuery1.Eof do begin
  ComboBox1.Items.Add(ADOQuery1.Fields[1].AsString);
  ADOQuery1.Next;
end;
end;

procedure TForm1.Button3Click(Sender: TObject);
begin
ADOQuery1.Append;
ADOQuery1.FieldByName('URL').AsString:=Edit2.Text;
ComboBox1.Items.Clear;
ADOQuery1.First;
while not ADOQuery1.Eof do begin
  ComboBox1.Items.Add(ADOQuery1.Fields[1].AsString);
  ADOQuery1.Next;
end;
end;

procedure TForm1.FormCreate(Sender: TObject);
var DatabaseFileName: string;
    s: string;
    path: string;
begin
s:=paramStr(0);
path:=ExtractFilePath(s);
DatabaseFileName := path+'Requester.mdb';
ADOConnection1.ConnectionString:='Provider=Microsoft.Jet.OLEDB.4.0;Data Source='+DatabaseFileName+';Persist Security Info=False';
ADOQuery1.Open;
ADOQuery1.First;
while not ADOQuery1.Eof do begin
  ComboBox1.Items.Add(ADOQuery1.Fields[1].AsString);
  ADOQuery1.Next;
end;
end;

end.
