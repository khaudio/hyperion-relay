#include <iostream>
#include <string>
#include <regex>
#include "subprocess.hpp"

using namespace std;

int main()
{
    subprocess::popen proc("hyperion-remote", {"-l"});
    string status(static_cast<stringstream const&>(stringstream() << proc.stdout().rdbuf()).str());

    std::regex h("\"HEX Value\" : .+,");
    std::smatch val;

    std::regex_search(status, val, h);
    for (size_t i = 0; i < val.size(); ++i)
        cout << val[i] << endl;

    return 0;
}
