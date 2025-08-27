#include "doconfig.h"
#include <iostream>
#include <fstream>
#include <QDebug>
/*
    "line1" : "Windows Hacked",
    "line2" : "Go to http://127.0.0.1 to pay the ransom.",
    "port" : 20520,
    "ratio" : {
        "up" : 8,
        "down" : 1,
        "right" : 1,
        "left" : 20
    }
*/
// 使用 nlohmann 命名空间
using json = nlohmann::json;
using namespace std;

void to_json(json &j, const Data &d)
{
    j = json{{"line1", d.line1}, {"line2", d.line2}, {"port", d.port}, {"ratio", d.ratio}};
}

void from_json(const json &j, Data &d)
{
    j.at("line1").get_to(d.line1);
    j.at("line2").get_to(d.line2);
    j.at("port").get_to(d.port);
    j.at("ratio").get_to(d.ratio);
}

Data setupConfig()
{
    Data data;
    data.line1 = "激活 Windows";
    data.line2 = "转到\"设置\"以激活 Windows。";
    data.port = 20520;
    map<string, int> r;
    r.insert(pair<string, int>("up", 8));
    r.insert(pair<string, int>("down", 1));
    r.insert(pair<string, int>("right", 1));
    r.insert(pair<string, int>("left", 20));
    data.ratio.swap(r);
    json jsonData = data;
    // 转换为字符串
    string prettyString = jsonData.dump(4); // 带缩进的格式（4个空格）

    qWarning() << "Pretty JSON:\n"
               << prettyString << "\n\n";

    // 写入文件
    ofstream o("user.json", ios::out);
    o << prettyString << endl;
    o.close();
    return data;
}

Data readConfig()
{
    if (!ifstream("user.json").is_open())
    {
        return setupConfig();
    }
    ifstream i("user.json", ios::in);
    json jsonData;
    i >> jsonData;
    Data data;
    jsonData.get_to(data);
    i.close();
    return data;
}
