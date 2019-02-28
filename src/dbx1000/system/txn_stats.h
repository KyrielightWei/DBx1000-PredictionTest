/*collect some information for txn runing in the system*/

#ifndef TXN_STATS
#include TXN_STATS

#include "global.h"
#include "txn.h"

#include <map>

using std::map;

struct EachTxnStats //map
{
    /*CPU time*/
    double cpu_time;
    /*memory size*/
    uint64_t me_size;
    /*io data size*/
    uint64_t read_size;
    uint64_t write_size;
    uint32_t read_count;
    uint32_t write_count;
    /*io time*/
    double io_time;
};

enum TXN_STATS_TYPE
{
    CPU_TIME,
    MEMORY,
    READ_SIZE,
    READ_CNT,
    WRITE_SIZE,
    WRITE_CNT,
    IO_TIME
}


class TxnStats
{
    private:

    map<txnid_t,EachTxnStats*> txn_infor_map;

    public:

    void init();
    
    static void clearStats(EachTxnStats * txn_stats); // init each_txn_stats

    void add_stats(txnid_t txn_id,TXN_STATS_TYPE type,void * value);

    bool add_txn(txnid_t txn_id);
}


#endif