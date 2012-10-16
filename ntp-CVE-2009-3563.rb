#Author: Gursev Singh Kalra
require 'socket'
TIMEOUT = 5 

if(ARGV.count != 1)
	puts "[-] Target host not provided. Usage: ntp.rb <target_server>"
	exit
end

target_server = ARGV[0]
target_port = 123

socket = nil
response = nil

begin
	test_string = "\x97\x00\x00\x00\xAA\x00\x00\x00"
	socket = UDPSocket.open
	socket.send(test_string, 0, target_server, target_port)
	if select([socket], nil, nil, TIMEOUT)
		response = socket.recvfrom(10)
	end
rescue (IOError ex)
	puts ex.to_s
ensure
	socket.close if(socket)
end

if(response && response[0].index("\x97\x00\x00\x00"))
	puts "[+] Vulnerable to NTP Mode 7 Request Denial Of Service"
else
	puts "[-] Not vulnerable to NTP Mode 7 Request Denial Of Service"
end
