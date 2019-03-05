#include "txn_stats.h"
#include "ycsb_query.h"
#include "ycsb.h"

#define BILLION 1000000000UL

TxnStats txn_stats;

void TxnStats::clearStats(EachTxnStats * txn_stats)
{
    txn_stats->cpu_time = 0;
    txn_stats->me_size = 0;
    txn_stats->read_keys.clear();
    txn_stats->write_keys.clear();
    txn_stats->scan_keys.clear();
    //txn_stats->_type = 0;
    txn_stats->rc = RCOK;
    txn_stats->start_time = 0;
    //txn_stats->io_time = 0;
}

void TxnStats::init()
{
    //insert_latch = false;
    
    pthread_mutex_init(&insert_txn_mutex,NULL);
    txn_infor_map.clear();
}

void TxnStats::add_stats(txnid_t txn_id,TXN_STATS_TYPE type,void * value)
{
    //cout << type << endl;
    /*if(type ==  READ_KEY)
    {
        cout << "READ:" << txn_id << endl;
    }
    if(type == WRITE_KEY)
    {
        cout << "WRITE:" << txn_id << endl;
    }*/
    /*if(txn_infor_map.find(txn_id) == txn_infor_map.end())
    {   // add_txn(txn_id);
        cout << "not fond id : "<<txn_id << endl;
        bool id_not_found = true;
        assert(!id_not_found);
    }*/
    if(txn_infor_map.find(txn_id) == txn_infor_map.end())
    {
        add_txn(txn_id);
    }

    EachTxnStats * txn_stats = txn_infor_map[txn_id];
   // map<key_type,uint32_t> * keys = NULL;
    ScanInfo * s = NULL;
    switch (type)
    {
        case CPU_TIME:
            txn_stats->cpu_time += *((uint64_t*)value);
            break;
        case MEMORY:
            txn_stats->me_size += *((UInt64*)value);
            break;
        case READ_KEY:
            txn_stats->read_keys[*(key_type*)value]++;
            break;
        case WRITE_KEY:
            txn_stats->write_keys[*(key_type*)value]++;
            break;
        case SCAN_KEY:
            s = (ScanInfo*)value;
            txn_stats->scan_keys[s->scan_key] += s->scan_len; 
            break;
        case TXN_TYPE:
            txn_stats->_type = *(MyTxnType*)value;
            break;
        case START_TIME:
            txn_stats->start_time = *(uint64_t*)value;
            break;
        case RESULT:
            txn_stats->rc = *(RC*)value;
            break;
        default:
            bool type_not_found = true;
            ASSERT(!type_not_found);
            break;
    }
    /*if(keys != NULL)
    {
        if (keys->find((key_type)*value) == keys.end()) 
        {
            (*keys)[*value] = 0;
        }
        (*key)[*value]++;
    }*/
}

bool TxnStats::add_txn(txnid_t txn_id)
{
    //while ( !ATOM_CAS(insert_latch, false, true) ) {}
  

    if(txn_infor_map.find(txn_id) != txn_infor_map.end())
    {  
       // cout << "have txn - " << txn_id << endl;
        return false;
    }
    //cout << "have txn" << txn_id << endl;
    pthread_mutex_lock(&insert_txn_mutex);
    EachTxnStats * temp_stats = (EachTxnStats*)mem_allocator.alloc(sizeof(EachTxnStats),0);
    clearStats(temp_stats);
    txn_infor_map[txn_id] = temp_stats; 

    pthread_mutex_unlock(&insert_txn_mutex);
    //ATOM_CAS(insert_latch, true, false);
    
    return true;
}

void TxnStats::final_type_cal(uint8_t * final_type,access_t rtype)
{
    uint8_t temp_type = 0;
    switch (rtype)
    {
        case RD:
            temp_type = 1;
            break;
        case WR:
            temp_type = 2;
            break;
        case SCAN:
            temp_type = 3;
            break;
        default:
            assert(false);
            break;
    }
    if((temp_type<3 && *final_type <3) || (temp_type>=3 && *final_type>=3))
    {
        *final_type = temp_type > *final_type ? temp_type:*final_type;
    }
    else
    {
        if(*final_type < 3) //temp_type = 3
        {
            *final_type = *final_type + 3;
        }
        else //temptype < 3 && finaltype>=3
        {
            *final_type = *final_type - 3;
            *final_type = temp_type > *final_type ? temp_type:*final_type;
            *final_type = *final_type + 3;
        }
    }
}


void TxnStats::txn_finish(txn_man * txn,base_query* query,RC rc,uint64_t timespan,uint64_t start_time)
{
    txnid_t txn_id = txn->get_txn_id();
   // cout << "txn:" << txn_id << endl;
   	
    if(txn_infor_map.find(txn_id) == txn_infor_map.end())
    {  
        add_txn(txn_id);
    }
    
   /* if(txn_infor_map.find(txn_id) == txn_infor_map.end())
    {
        cout << "none:" << txn_id << endl;
    }*/
    

    /*if(!add_txn(txn_id))
    {
        cout << "already have txn : " << txn_id << endl;
        bool id_insert_fail = false;
        assert(id_insert_fail);
    }*/


    add_stats(txn_id,RESULT,&rc);
    add_stats(txn_id,CPU_TIME,&timespan);
    add_stats(txn_id,START_TIME,&start_time);

#if WORKLOAD == YCSB
    uint8_t final_type = 0;

    ycsb_query * now_query = (ycsb_query*)query;
    ycsb_request * req = now_query->requests;
    //cout << now_query->request_cnt << endl;
    for(uint64_t i = 0; i < now_query->request_cnt; i++)
    {
        final_type_cal(&final_type,req[i].rtype);
        if(req[i].rtype == RD)
        {
            add_stats(txn_id,READ_KEY,&req[i].key);
        }
        else if (req[i].rtype == WR) 
        {
            add_stats(txn_id,WRITE_KEY,&req[i].key);
        }
        else if(req[i].rtype == SCAN)
        {
            ScanInfo s;
            s.scan_key = req[i].key;
            s.scan_len = req[i].scan_len;
            add_stats(txn_id,SCAN_KEY,&s);
        }
    }

    MyTxnType txn_type;
    switch (final_type)
    {
        case 1:
            txn_type = TXN_READ;
            break;
        case 2:
            txn_type = TXN_WR;
            break;
        case 3:
            txn_type = TXN_SCAN;
            break;
        case 4:
            txn_type = SCAN_READ;
            break;
         case 5:
            txn_type = SCAN_WR;
            break;
        default:
            assert(false);
            break;
    }

    add_stats(txn_id,TXN_TYPE,&txn_type);
#endif

}

void TxnStats::stats_print()
{
    for(TxnMap::iterator i = txn_infor_map.begin(); i != txn_infor_map.end(); i++)
    {
        txnid_t txn_id = i->first;
        EachTxnStats * now_stats = i->second;
        cout << endl;
        cout << "TXN_ID = " << txn_id << endl;
        cout << "CPU_TIME = " << now_stats->cpu_time  << endl;
        cout << "START_TIME = " << now_stats->start_time << endl;
        cout << "TXN_RESULT = " << convertToStr(RESULT,&now_stats->rc)<< endl;
        cout << "TXN_TYPE = " << convertToStr(TXN_TYPE,&now_stats->_type) << endl;
        cout << "READ_COUNT = " << now_stats->read_keys.size() << endl;
        cout << "WRITE_COUNT = " << now_stats->write_keys.size() << endl;
        cout << "SCAN_COUNT = " << now_stats->scan_keys.size() << endl;
    }
    
}

string TxnStats::convertToStr(TXN_STATS_TYPE type,void * value)
{
    switch (type)
    {
        case RESULT:
            switch (*(RC*)value)
            {
                case RCOK:
                    return "OK";
                    break;
                case Abort:
                    return "Abort";
                    break;
                default:
                    return "Unknown";
                    break;
            }
        case TXN_TYPE:
            switch (*(MyTxnType*)value)
            {
                case TXN_READ:
                    return "READ";
                    break;
                case TXN_WR:
                    return "WR";
                    break;
                case TXN_SCAN:
                    return "SCAN";
                    break;
                case SCAN_READ:
                    return "SCAN_READ";
                    break;
                case SCAN_WR:
                    return "SCAN_WR";
                    break;
                default:
                    return "Unknown";
                    break;
            }
    
        default:
            return "ERROR";
            break;
    }
}