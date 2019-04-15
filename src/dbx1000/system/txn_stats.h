/*collect some information for txn runing in the system*/

#ifndef TXN_STATS
#define TXN_STATS

#include "global.h"
#include "txn.h"
#include "mem_alloc.h"

#include <map>
#include <vector>

typedef uint64_t key_type;

enum MyTxnType
{
    TXN_READ,  //1
    TXN_WR,  //2
    TXN_SCAN,   //3
    SCAN_READ, // 1+3 
    SCAN_WR //2+3
};

struct EachTxnStats //map
{
    /*CPU time*/
    uint64_t cpu_time;
    /*memory size*/
    uint64_t me_size;
    /*WR*/
    map<key_type,uint32_t> read_keys;
    map<key_type,uint32_t> write_keys;
    map<key_type,uint32_t> scan_keys; // start_key and scan_len
    /*access type*/
    MyTxnType _type;
    /*result*/
    RC rc;
    /*start time*/
    uint64_t start_time;
    /*start time*/
    uint64_t get_query_time;
    uint64_t index_time;
    uint64_t cc_time;
};

enum TXN_STATS_TYPE
{
    CPU_TIME,
    MEMORY,
    READ_KEY,
    WRITE_KEY,
    SCAN_KEY,
    TXN_TYPE,
    RESULT,
    START_TIME,
    GET_QUERY_TIME,
    INDEX_TIME,
    CC_TIME
};

struct ScanInfo
{
    key_type scan_key;
    uint32_t scan_len;
};

typedef map<txnid_t,EachTxnStats*> TxnMap;

class TxnStats
{
    private:

    map<txnid_t,EachTxnStats*> txn_infor_map;

    pthread_mutex_t insert_txn_mutex;
    //bool insert_latch;
    //bool key_count_latch;

    public:

    void init();
    
    static void clearStats(EachTxnStats * txn_stats); // init each_txn_stats

    void add_stats(txnid_t txn_id,TXN_STATS_TYPE type,void * value);

    bool add_txn(txnid_t txn_id);

    void final_type_cal(uint8_t * final_type,access_t rtype);

    void txn_finish(txn_man * txn,base_query* query,RC rc,uint64_t timespan,uint64_t start_time,uint64_t query_time,RunInfor infor);

    
    void stats_print();

    string convertToStr(TXN_STATS_TYPE type,void * value);
};

extern TxnStats txn_stats;

#endif