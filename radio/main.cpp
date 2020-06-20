#include <sqlite3.h>
#include <iostream>

static int callback(void* data, int argc, char** argv, char** azColName);
void basicSelect();

int main() {
	basicSelect();
	return 0;
}

static int callback(void* data, int numRows, char** rows, char** colNames) {
	std::cout << (const char*)data << std::endl;

	for (int i = 0; i < numRows; ++i) {
		std::cout << colNames[i] << " = " << rows[i] << std::endl;
	}
	return 0;
}

void basicSelect() {
	sqlite3* db;
	int exit = 0;
	exit = sqlite3_open("../db.sqlite3", &db);
	std::string data = "CALLBACK FUNCTION";
	std::string sql = "SELECT * FROM boom_deploy;";

	if (exit) {
		std::cout << "failure" << std::endl;
	}
	else {
		std::cout << "success" << std::endl;
	}

	int rc = sqlite3_exec(db, sql.c_str(), callback, (void*)data.c_str(), NULL);
	if (rc != SQLITE_OK)
		std::cout << "ERROR SELECT" << std::endl;
	else
		std::cout << "OPERATION OK!" << std::endl;
	
	sqlite3_close(db);
}
