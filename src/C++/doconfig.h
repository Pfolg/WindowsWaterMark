#ifndef DOCONFIG_H
#define DOCONFIG_H

#include <string>
#include <map>
#include "json.hpp" // 包含 json 库（确保路径正确）

// 使用 nlohmann 命名空间
using json = nlohmann::json;
using namespace std;

struct Data
{
    string line1;
    string line2;
    int port;
    map<string, int> ratio;
};
void to_json(json &j, const Data &d);
void from_json(const json &j, Data &d);
Data setupConfig();
Data readConfig();

#endif // DOCONFIG_H
