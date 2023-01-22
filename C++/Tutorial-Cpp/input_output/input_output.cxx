////////////////////////////////////////////////////////////////////////////////
// Useful References
// http://www.cplusplus.com/doc/tutorial/files/
// https://www.cprogramming.com/tutorial/c++-iostreams.html
// https://www.learncpp.com/cpp-tutorial/input-and-output-io-streams/
// https://www3.ntu.edu.sg/home/ehchua/programming/cpp/cp10_IO.html
////////////////////////////////////////////////////////////////////////////////

#include <iostream>
using std::cin;
using std::cout;
using std::cerr;
using std::clog;
using std::endl;
using std::flush;
#include <istream>
using std::istream;
#include <sstream>
using std::stringstream;
#include <fstream>
using std::ofstream;
using std::ifstream;
using std::getline;
using std::ios;
#include <string>
using std::string;
#include <limits>
using std::numeric_limits;
//const long int STREAM_MAX = numeric_limits<std::streamsize>::max();

// Globals
string m_ofile1_path      = "./test_output_file1.txt";
string m_ofile2_path      = "./test_output_file2.txt";
string m_ifile_path       = "./test_input_file.txt";
string m_nonexistent_file = "non_existent_file.foo";

// Function declaration
void print_stream_status(const ofstream& ofs, const string file_path = "");
void print_stream_status(const ifstream& ifs, const string file_path = "");

istream& getline(istream& ss, stringstream& o_ss) {
    string line;
    getline(ss, line);
    o_ss.str("");
    o_ss.clear();
    o_ss << line;
    return ss;
}
////////////////////////////////////////////////////////////////////////////////
int main() {

    ////////////////////////////////////////////////////////////////////////////
    // Console streams
    cout << "Hello Console I/O from cout (stdout ostream)" << endl;
    clog << "Hello Console I/O from clog (buffered stderr ostream)" << endl;
    cerr << "Hello Console I/O from cerr (unbuffered stderr ostream)" << endl;

    // endl vs flush?
    cout << "endl" << endl;
    cout << "flush\n" << flush;

    ////////////////////////////////////////////////////////////////////////////
    // File streams

    // Initialize output file stream
    ofstream ofs;
    print_stream_status(ofs);

    // Open output file and clear any previous content
    ofs.open(m_ofile1_path, std::ios::trunc);
    print_stream_status(ofs, m_ofile1_path);

    // Initialize input file stream
    ifstream ifs;
    print_stream_status(ifs);
    
    // Open non-existent input file
    ifs.open(m_nonexistent_file);
    print_stream_status(ifs, m_nonexistent_file);
    
    // Open actual input file
    ifs.open(m_ifile_path);
    print_stream_status(ifs, m_ifile_path);
    
    // Move "get position" to end of file
    //ifs.seekg(0, ios::end);
    //print_stream_status(ifs, m_ifile_path);

    // Read input file content into string
    string ifs_readout;
    if (ifs.good() && ifs.is_open()) {
        string line;
        while (getline(ifs, line) ) {
            ifs_readout += line;
        }
        print_stream_status(ifs, m_ifile_path);
        ifs.close();
    }

    // Write to output file
    if (ofs.good() && ofs.is_open()) { 
        ofs << "Hello output file 1 from ofstream." << endl;
        ofs << "ifstream says \"" << ifs_readout << "\"." << endl; 
        ofs.close(); // Must close ofstream in order to reassign it
    }

    // Open different file with same output file stream
    ofs.open(m_ofile2_path, std::ios::trunc);
    if (ofs.good() && ofs.is_open()) { 
        ofs << "Hello output file 2 from ofstream" << endl;
        ofs.close();
    }

    ////////////////////////////////////////////////////////////////////////////
    // Input streams
    // cin << 
    // cin.get()
    // cin.getline() and cin.count()
    // std::getline(std::cin, strBuf)
    // cin.ignore(n)
    // cin.peek()
    // cin.unget()
    // cin.putback()

    ////////////////////////////////////////////////////////////////////////////
    // String streams

    // Initialize
    stringstream ss;

    // Insert
    ss << "Hello console I/O from stringstream";

    // Read into string
    cout << ss.str() << endl;

    // Insert
    ss << "\n";
    ss << "Block 1\n";
    ss << "1 2 3\n";
    ss << "4 5 6\n";
    ss << "7 8 9\n";
    ss << "\n";
    ss << "Block 2\n";
    ss << "1 2 3\n";
    ss << "4 5 6\n";
    ss << "7 8 9\n";
   
    // Read multiple lines
    //string line;
    //while (getline(ss, line)) { cout << line << endl; }
    stringstream line_ss;
    while (getline(ss, line_ss)) { 
        string s;
        line_ss >> s;
        cout << s << "; eof = " << ss.eof() << endl; 
    }
    cout << "eof = " << ss.eof() << endl; 

    // IO Manipulators
    // setw

    ////////////////////////////////////////////////////////////////////////////
    // END
    return 0;
}

void print_stream_status(const ofstream& ofs, const string file_path) {
    if ( file_path == "" ) {
        cout << "Is ofstream " << flush;
    } else {
        cout << "Is ofstream for " << file_path << " " << flush;
    }
    cout << "good? " << (ofs.good()    ? "Yes" : "No") << "; "
         << "open? " << (ofs.is_open() ? "Yes" : "No") << "; "
         << "eof? "  << (ofs.eof()     ? "Yes" : "No") << "; "
         << "bad? "  << (ofs.bad()     ? "Yes" : "No") << "; "
         << "fail? " << (ofs.fail()    ? "Yes" : "No") << "; "
         << endl;
}
void print_stream_status(const ifstream& ifs, const string file_path) {
    if ( file_path == "" ) {
        cout << "Is ifstream " << flush;
    } else {
        cout << "Is ifstream for " << file_path << " " << flush;
    }
    cout << "good? " << (ifs.good()    ? "Yes" : "No") << "; "
         << "open? " << (ifs.is_open() ? "Yes" : "No") << "; "
         << "eof? "  << (ifs.eof()     ? "Yes" : "No") << "; "
         << "bad? "  << (ifs.bad()     ? "Yes" : "No") << "; "
         << "fail? " << (ifs.fail()    ? "Yes" : "No") << "; "
         << endl;
}
