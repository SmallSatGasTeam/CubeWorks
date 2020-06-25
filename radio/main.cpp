#include <iostream>

#include "radioDriver.hpp"

int main() {
	RadioDriver test(0);
	test.queryDB(false, "SELECT * FROM ttnc;");
	return 0;
}


