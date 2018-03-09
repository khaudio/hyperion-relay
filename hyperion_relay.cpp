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
    const int relay = 2, ledStatus = 21, ledPower = 3;
    const int pins[3] = {relay, ledStatus, ledPower}
    wiringPiSetupGpio();
    for (int i = 0; i < pins.size(); i++)
    {
        pinMode(pins[i], OUTPUT);
        digitalWrite(pins[i], 1);
    }

    string status, color;
    bool on, last;
    std::smatch val;
    std::regex h("\"HEX Value\" : \\[ \"(.+)\"");

    while (true)
    {
        subprocess::popen proc("hyperion-remote", {"-l"});
        status = (static_cast < stringstream const & > (stringstream() << proc.stdout().rdbuf()).str());

        std::regex_search(status, val, h);
        color = &val[1];
        on = !color.empty();

	if (on != last)
        {
            cout << "Lights " << ((on) ? "on" : "off") << endl;
            digitalWrite(2, ((on) ? 0 : 1));
        }

	last = on;
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
    return 0;
}
