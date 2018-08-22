#include<bits/stdc++.h>
#include<string.h>

using namespace std;


// int calc_factorial(int n){
// 	int ans=1;
// 	int i;
// 	for(i=1;i<=n;i++){
// 		ans=ans*i;
// 	}
// 	return(ans);
// }


set<char> delimiters = {' ' ,'+' ,'-' ,'*' ,'/' ,',' ,';' ,'>' ,'<' ,'=', '(' ,')' ,'[' ,']' ,'{' ,'}' };
set<char> operators= {'+', '-', '*', '/', '>' ,'<' ,'=' ,'&' ,'|' ,'^' };
set<char> integers= {'0','1','2','3','4','5','6','7','8','9'};
set<string> keywords={"if", "else", "while", "do", "break", "continue", "int", "double","float" ,"return" ,"char" ,"case" ,"char" ,"sizeof" ,"long" ,"short" ,"typedef" ,"switch" ,"unsigned" ,"void" ,"static" ,"struct", "goto" };


//Answer Set
set<string> ints;
set<string> realnos;
set<string> keywrds;
set<string> validIdentifrs;
set<char> opersUsed;

string find_substr(string s,int l,int r){
	string ans="";
	for(int i=l;i<=r;i++){
		ans=ans+s[i];
	}
	return(ans);
}

bool is_keyword(string x){
	if(keywords.find(x)!=keywords.end()){
		return(true);
	}
	else{
		return(false);
	}
}

bool is_integer(string x){
	int len=x.length();
	if(len==0){
		return(false);
	}
	for(int i=0;i<len;i++){
		if(integers.find(x[i])==integers.end() || (x[i]=='-' && i>0)){
			return(false);
		}
	}
	return(true);	
}
bool is_realno(string x){
	int len=x.length();
	if(len==0){
		return(false);
	}
	bool flag=false;
	for(int i=0;i<len;i++){
		if(integers.find(x[i])==integers.end() && x[i]!='.' || (x[i]=='-' && i>0)){
			return(false);
		}
		if(x[i]=='.'){
			flag=true;
		}
	}
	return(flag);
}

bool is_validIdentifier(string x){
	if(integers.find(x[0])!=integers.end() || delimiters.find(x[0])!=delimiters.end()){
		return(false);
	}
	return(true);
}

void lexical_parser(string s){
	int start=0;
	int end=0;
	int len=s.length();

	// if(delimiters.find('+')!=delimiters.end()){
	// 	cout << "true";
	// }

	while(start<=end && end<=len ){
		//cout << start << " " << end << endl;
		if( delimiters.find(s[end])==delimiters.end() ){
			end+=1;
		}

		if(delimiters.find(s[end])!=delimiters.end() && start==end){
			if(operators.find(s[end])!=operators.end()){
				cout << s[end] << " is an Operator" << endl;
				opersUsed.insert(s[end]);
			}
			end++;
			start=end;
		}
		else if(  delimiters.find(s[end])!=delimiters.end() && start!=end  || (end==len && start!=end)){
			string substr= find_substr(s,start,end-1);

			if(is_keyword(substr)==true){
				cout << substr << " is a Keyword" << endl;
				keywrds.insert(substr);
			}
			else if(is_integer(substr)==true){
				cout << substr << " is a Integer" << endl;
				ints.insert(substr);	
			}
			else if(is_realno(substr)==true){
				cout << substr << " is a Real Number" << endl;
				realnos.insert(substr);	
			}
			else if(is_validIdentifier(substr)==true && delimiters.find(s[end-1])==delimiters.end()){
				cout << substr << " is a Valid Identifier" << endl;
				validIdentifrs.insert(substr);
			}
			else if(is_validIdentifier(substr)==false && delimiters.find(s[end-1])==delimiters.end() ){
				cout << substr << " is not a Valid identifier" << endl;	
			}
			//end++;
			start=end;
		}

	}

	return;

}








int main(){
	string str1="int calc_factorial(int n){int ans=1; int i; for(i=1;i<=n;i++){ ans=ans*i; } return(ans); }";
	string str2="int a=b+2;";	
	lexical_parser(str1);

	cout << endl << "*** List of Keywords in given program :-" << endl;
	for(auto it=keywrds.begin();it!=keywrds.end();it++){
		cout << (*it) << endl;
	}
	
	cout << endl << "*** List of Valid Identifiers in given program :-" << endl;	
	for(auto it=validIdentifrs.begin();it!=validIdentifrs.end();it++){
		cout << (*it) << endl;
	}

	cout << endl << "*** List of Integers in given program :-" << endl;
	for(auto it=ints.begin();it!=ints.end();it++){
		cout << (*it) << endl;
	}

	cout << endl << "*** List of Real Numbers in given program :-" << endl;	
	for(auto it=realnos.begin();it!=realnos.end();it++){
		cout << (*it) << endl;
	}
	
	cout << endl << "*** List of operators in given program :-" << endl;
	for(auto it=opersUsed.begin();it!=opersUsed.end();it++){
		cout << (*it) << endl;
	}
}
