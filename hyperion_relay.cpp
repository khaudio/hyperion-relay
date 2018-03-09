#include <iostream>
#include <string>
#include <regex>
#include <thread>
#include <chrono>
#include <wiringPi.h>
#include "subprocess.hpp"

using namespace std;

int main()
{
    int relay = 2;
    wiringPiSetupGpio();
    pinMode(2, OUTPUT);
    pinMode(21, OUTPUT);
    pinMode(3, OUTPUT);

    digitalWrite(21, 1);
    digitalWrite(3, 1);
    digitalWrite(2, 1); 

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
            digitalWrite(2, ((on) ? LOW : HIGH));
        }

	last = on;
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
    return 0;
}
