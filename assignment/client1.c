#include <fstream>
#include <string>
#include <cstdio>
#include <iostream>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>

int main(void)
{
	int sockfd = 0;
	int bytesReceived = 0,n;
	char recvBuff[256],input[256];
	//memset(recvBuff,'0',sizeof(recvBuff));
	struct sockaddr_in serv_addr;

        sockfd = socket(AF_INET, SOCK_DGRAM, 0);	
        printf("%d\n",sockfd);
	std::cout << "Please input what file you want to send ...\n";

	std::cout << "> ";
	std::cin >> input;

	//create a socket first.
	if (sockfd==0)
	{
		printf("Error : could not create socket.");
		return 1;
	}

	// Initialize socaddr attributes
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_port = htons(9001);
	serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

	std::ifstream file(input);
	std::string s;
	//int res = connect(sockfd, (sockaddr *) &serv_addr,sizeof(serv_addr));
	while (std::getline(file,s))
	{
		//int res = connect(sockfd, (sockaddr *) &serv_addr, sizeof(serv_addr));
		//printf("%d\n",res);
		//if (res == -1)
		//{
		//	printf("ERROR, cleanup failed.");
		//	return 1;
		//}
		
		
		printf("%s\n", s.c_str());
		sendto(sockfd, s.data(),s.size(),0,(struct sockaddr*)&serv_addr,sizeof(serv_addr));
		//n = write(sockfd, s.data(), s.size(), 0);	
	}
    return 0;
}
