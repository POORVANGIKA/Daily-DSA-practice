//You are given two integers N and F
//Your task is to check whether F
 //is a factor of N
 
 #include<iostream>
 using namespace std;
 
 int main (){
 	long long N,F;
 	cout<<"enter the two integers";
 	cin>>N>>F;
 	if (N%F==0){
 		cout<<"yes";
	 }
	 else{
	 	cout<<"no";
	 }
 }


