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
    const int pins[3] = {2, 3, 21};
    const int relay = pins[0], ledStatus = pins[1], ledPower = pins[2];
    const std::regex hexVal("\"HEX Value\" : \\[ \"(.+)\"");
    string status;
    bool on, last;
    std::smatch state;

    wiringPiSetupGpio();

    // Set the pins as outputs
    for (int i = 0; i < 3; i++)
    {
        pinMode(pins[i], OUTPUT);
        digitalWrite(pins[i], 1);
    }

    // Flash the status LED
    for (int i = 2; i < 6; i++)
    {
        digitalWrite(ledStatus, (i % 2));
        std::this_thread::sleep_for(std::chrono::milliseconds(250));
    }

    while (true)
    {
        subprocess::popen proc("hyperion-remote", {"-l"});
        status = (static_cast < stringstream const & > (stringstream() << proc.stdout().rdbuf()).str());
        std::regex_search(status, state, hexVal);
        on = !((string)(state[1])).empty();

	if (on != last)
        {
            cout << "Lights " << ((on) ? "on" : "off") << endl;
            digitalWrite(relay, ((on) ? 0 : 1));
            last = on;
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
    return 0;
}
