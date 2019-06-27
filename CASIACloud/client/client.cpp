#include <cpprest/http_client.h>
#include <cpprest/filestream.h>
#include <cpprest/json.h>
#include <boost/algorithm/string/replace.hpp>
#include <sys/time.h>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/md5.h>
using namespace utility;                    // Common utilities like string conversions
using namespace web;                        // Common features like URIs.
using namespace web::http;                  // Common HTTP functionality
using namespace web::http::client;          // HTTP client features
using namespace concurrency::streams;       // Asynchronous streams
using namespace std;

class Client{
public:
        string id;
        string password;
        void login_screen();
        int  login(string id, string password);
        bool login_status(json::value const & value);
        void json_post(json::value json_v);

        void my_print_results(json::value const & value);
        void http_status(int status_code);
private:
        // string id;
        // string password;
};

void Client::login_screen()
{
    cout<<"Please input your username and password\n";
    cin>>this->id>>this->password;
}

int Client::login(string id,string password){
    int login_status;
    json::value post_login;
    post_login["id"] = json::value::string(id);
    post_login["password"] = json::value::string(password);

    http_client client(U("http://127.0.0.1:8000/"));
    uri_builder builder(U("api/device/"));
    client
    // send the HTTP GET request asynchronous
    .request(methods::POST,builder.to_string(),post_login)
    // continue when the response is available
    .then([&](http_response response) -> pplx::task<json::value> {
        // if the status is OK extract the body of the response into a JSON value
        // works only when the content type is application\json
        cout<<"post.request: "<<response.status_code()<<endl;
        if(response.status_code() == status_codes::OK) { //Created?
            cout<<"ok!!!\n";
            response.headers().set_content_type("application/json"); //fixed June 22th
            return response.extract_json();
        }
        // return an empty JSON value
        return pplx::task_from_result(json::value());
    })
    .then([&](pplx::task<json::value> previousTask) {
        try
        {
            cout<<"connect to client"<<endl;
            json::value jv = previousTask.get();
            this->login_status(jv);
            login_status=1;  //my print result parameter
        }
        catch (const std::exception& e)
        {
        cout<<"error!\n";
            cout << e.what() << endl;
        }
    })
    .wait();

    return login_status;
}

bool Client::login_status(json::value const & value){
    cout<<"--------------------login  status--------------------"<<endl;
    if(value.size()){
        //auto obj =value.as_object();
        auto code = value.at(U("code")).as_integer();
        auto reason = value.at(U("reason")).as_string();
        auto state = value.at(U("state")).as_string();
        cout << "code = " << code <<endl
        << "reason = " << reason <<endl
        << "state = " << state << endl;
        if(state=="fail") return false;
        else return true;
      }
    cout<<"--------------------------End--------------------------"<<endl;

}

/*
void Client::my_print_results(json::value const & value)
{
    cout<<"--------------------Print--------------------"<<endl;
    if(value.size()){
        if(value.is_array()){
            auto array=value.as_array();
            for(auto iter = array.begin();iter!=array.end();++iter ){
                auto data = *iter;
                auto dataobj=data.as_object();
                 for (auto iterInner = dataobj.cbegin(); iterInner != dataobj.cend(); ++iterInner) {
                    auto &propertyName = iterInner->first;
                    auto &propertyValue = iterInner->second;
                    cout << propertyName << ", Value: " <<
                    propertyValue << std::endl;
                 }
            }
        }
        else if (value.is_string()) {
                cout<<"is string"<<endl;
        }
        else if(value.is_object()){
            auto obj =value.as_object();
            for (auto iterInner = obj.cbegin(); iterInner != obj.cend(); ++iterInner) {
                auto &propertyName = iterInner->first;
                auto &propertyValue = iterInner->second;
                cout << propertyName << ", Value: " <<
                propertyValue << std::endl;
            }
        }
        else  cout<<"not know what type it is"<<endl;
    }
    cout<<"---------------------End---------------------"<<endl;
}
*/

int main(){
        Client client;
        int login=0;
        do{
            int login = false;
            client.login_screen();
            login=client.login(client.id,client.password);
        }while(!login);

}

//c++ -o client -std=c++11 client.cpp -lcpprest -lboost_system -lssl -lcrypto
