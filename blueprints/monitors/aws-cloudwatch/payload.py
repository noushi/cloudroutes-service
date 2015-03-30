import boto.ec2.cloudwatch

import datetime
import ast

def check_each_dp(dp, threshold, m_type):
    for p in dp:
        val = p[m_type]
        if val > threshold:
            return True

    return False
    
    


def check(**kwargs):
    """ Checks Heroku's api status for dyno status"""
    jdata = kwargs['jdata']
    logger = kwargs['logger']

    region = jdata['region']
    name = 'CPUUtilization'
    m_type = 'Average'
    
    c = boto.ec2.cloudwatch.connect_to_region(region)
    

    name = 'CPUUtilization'
    m_type = 'Average'
#m_type = 'Maximum'
#m_type = 'Minimum' # in boto.ec2.cloudwatch.Metric.Statistics
    unit = 'Percent' # in boto.ec2.cloudwatch.Metric.Units

    dimension = { 'InstanceId' : [ 'i-feeac2f2' ]}
    dimension = ast.literal_eval(dimension)

    end = datetime.datetime.utcnow()
    start = end - datetime.timedelta(hours=24)
    
    metrics = c.list_metrics(metric_name=name, dimensions=dimension )
    
    m = metrics[0]

    dp = m.query(start, end, m_type)
    
    return check_each_dp(dp, threshold)
