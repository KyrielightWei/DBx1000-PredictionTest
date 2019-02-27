#include "txn_stats.h"

void TxnStats::clearStats(EachTxnStats * txn_stats)
{
    txn_stats->cpu_time = 0;
    txn_stats->read_size = 0;
    txn_stats->read_count = 0;
    txn_stats->write_count = 0;
    txn_stats->write_size = 0;
    txn_stats->io_time = 0;
}

void TxnStats::init()
{
    txn_infor_map.clear();
}

bool TxnStats::add_stats(txnid_t txn_id,TXN_STATS_TYPE type,void * value)
{
    switch (type)
    {
        case /* constant-expression */:
            /* code */
            break;
        case     :
            break;
    
        default:
            break;
    }
}