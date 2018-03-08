#include <iostream>
#include <string>
#include <regex>
#include <thread>
#include <chrono>
#include "subprocess.hpp"

using namespace std;

int main()
{
    string status, color;
    bool on, last;
    std::smatch val;
    std::regex h("\"HEX Value\" : \\[ \"(.+)\"");

    while (true)
    {
        subprocess::popen proc("hyperion-remote", {"-l"});
        status = (static_cast < stringstream const & > (stringstream() << proc.stdout().rdbuf()).str());

        std::regex_search(status, val, h);
        color = val[1];
        on = !color.empty();

	if (on != last)
        {
            cout << "Lights " << ((on) ? "on" : "off") << endl;
        }

	last = on;
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
    return 0;
}
