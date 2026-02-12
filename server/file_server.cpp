#include <iostream>
#include <fstream>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <cstring>

#pragma comment(lib, "ws2_32.lib")

#define PORT 9090
using namespace std;

void handleClient(SOCKET sock) {
    char buffer[1024] = {0};
    recv(sock, buffer, 1024, 0);
    string filename(buffer);
    ifstream file(filename);
    if (!file.is_open()) {
        string msg = "File not found\n";
        send(sock, msg.c_str(), msg.size(), 0);
    } else {
        string line;
        while (getline(file, line)) {
            line += "\n";
            send(sock, line.c_str(), line.size(), 0);
        }
        file.close();
    }
    closesocket(sock);
}

int main() {
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        cerr << "WSAStartup failed" << endl;
        return 1;
    }

    SOCKET server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd == INVALID_SOCKET) {
        cerr << "Socket creation failed" << endl;
        WSACleanup();
        return 1;
    }

    sockaddr_in address;
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    if (bind(server_fd, (sockaddr*)&address, sizeof(address)) == SOCKET_ERROR) {
        cerr << "Bind failed" << endl;
        closesocket(server_fd);
        WSACleanup();
        return 1;
    }

    if (listen(server_fd, 5) == SOCKET_ERROR) {
        cerr << "Listen failed" << endl;
        closesocket(server_fd);
        WSACleanup();
        return 1;
    }

    cout << "Server running on port " << PORT << endl;
    cout << "Press Ctrl+C to stop the server" << endl;

    while (true) {
        SOCKET new_socket = accept(server_fd, NULL, NULL);
        if (new_socket != INVALID_SOCKET) {
            handleClient(new_socket);
        }
    }

    closesocket(server_fd);
    WSACleanup();
    return 0;
}
