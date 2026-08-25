*** Settings ***
Documentation    座舱测试共享关键字库

*** Keywords ***
连接到CANoe
    [Arguments]    ${channel}=0    ${bitrate}=500000
    Log    连接CANoe: channel=${channel}, bitrate=${bitrate}
    # 实际项目中调用CANoe COM接口

发送CAN信号
    [Arguments]    ${signal_id}    ${value}
    Log    发送CAN信号: ${signal_id}=${value}

读取CAN信号
    [Arguments]    ${signal_id}
    Log    读取CAN信号: ${signal_id}
    RETURN    ${0}

启动UDS诊断会话
    [Arguments]    ${diagnostic_id}
    Log    启动UDS诊断会话: ${diagnostic_id}
    # 实际项目中调用udsoncan库

执行座舱语音命令
    [Arguments]    ${command}
    Log    执行语音命令: ${command}   