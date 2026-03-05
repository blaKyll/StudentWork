#include <iostream>//библиотека ввода/вывода
#include <string>//для работы со строками
#include <sstream>//для преобразования строк в числа 
#include <iomanip>//форматирования вывода

int a = 0;
int b = 0;
int result = 0;

//функция для ввода 16ти ричного числа, принимает строку-подсказку, возращает число в десятичном виде
int inputHex(std::string promt) {
	std::string input;
	int number;
	std::cout << promt;
	getline(std::cin, input);
	std::stringstream ss;//создаем поток для преобразования строки в число
	ss << std::hex << input;//записываем строку в поток, hex означает что число в 16ти ричной системе
	ss >> number;//преобразуем поток в число 
	return number;
}
//функция сложения на Assemblere, принимает два числа, возвращает их сумму 
int addAsm(int x, int y) {
	int result_asm = 0;
	__asm{
		mov eax, x//загружаем первое число в регистр abx
		mov ebx, y//загружаем второе число
		add eax,ebx//результат сложения будет в регистре eax
		mov result_asm, eax//сохраняем результат в eax в переменную
	}
	return result_asm;
}
int main()
{
	setlocale(LC_ALL, "ru");
	std::cout << "====================================" << std::endl;
	std::cout << "Введите числа в HEX (например:1F,A3,100)"<<std::endl;
	a = inputHex("Введите первое число в HEX:");
	b = inputHex("Введите второе число в HEX:");
	result = addAsm(a, b);
	std::cout <<"Результат:" << result;
	return 0;
}
