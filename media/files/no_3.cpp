#include <iostream>
#include <string>

using namespace std;

int main() {
    string biodata[5][2] = {
        {"m fari artha yudha", "202031048"},
        {"abdul hadi sadik", "201931157"},
        {"muhammad ilham farerik", "201931197"},
        {"salman rausyan fikri", "202031049"},
        {"muhammad fadhillah", "202031108"}
    };

    for (int i = 0; i < 5; i++) {
        if (biodata[i][1] == "202031049"){
            continue;
        } else {
            cout << "=== data ke "  << i+1 << " ===" << endl;
            cout << "nama : " << biodata[i][0] << endl;
            cout << "nim : " << biodata[i][1] << endl;
        }
    }
    
}