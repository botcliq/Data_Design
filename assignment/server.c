#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

//print error message
void error(const char *msg)
{
	//print message
	perror(msg);
	exit(1);
}


int main(int argc, char *argv[])
{
	// start variables
	int sockfd ,bytes_read , portno;
	socklen_t clilen;
	char buffer[256], recv_data[1024] , *addr;
	//structure required for address
	struct sockaddr_in serv_addr, cli_addr;
	int n;

	if (argc < 2) {
		fprintf(stderr,"ERROR, no port provided \n");
		exit(1);
	}
	
	//create the socket of type TCP
	sockfd = socket(AF_INET, SOCK_DGRAM, 0);
	if (sockfd <0)
		error("ERROR opening socket");
	
	//replace the pointer with zero values
	bzero((char *) &serv_addr, sizeof(serv_addr));
	//convert the portno value to integer
	portno = atoi(argv[2]);
	addr = argv[1];
	printf("addr : %s and port %d", addr, portno);
	// set server_addr attributes.
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = inet_addr(addr);
	serv_addr.sin_port = htons(portno);
	
        // bind the socket created with the serv_addr
	if (bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0)
		error("ERROR on binding");
	
	// start listening to the socket that we have created
	listen(sockfd,5);

        // set len of cli_addr 
	clilen = sizeof(cli_addr);
	while (1) {
		// accept any connection requests from the client.
		//newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
		bytes_read = recvfrom(sockfd,recv_data,102,0,(struct sockaddr *)&cli_addr,&clilen);
		recv_data[bytes_read] = '\0';
		printf("\n(%s , %d) sent:",inet_ntoa(cli_addr.sin_addr),ntohs(cli_addr.sin_port));
		printf("%s",recv_data);
		//fflush(stdout);
	}
	close(sockfd);
	return 0;
}
