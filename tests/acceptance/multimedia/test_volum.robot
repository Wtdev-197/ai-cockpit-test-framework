*** Settings ***
Documentation     座舱多媒体-音量调节验收测试
Resource          ../resources/common.resource
Resource          ../resources/cockpit_keywords.robot
Suite Setup       初始化测试环境
Suite Teardown    清理测试环境

*** Variables ***
# 模拟器内部状态（Mock模式用，真实环境接CANoe后删除）
${CURRENT_VOLUME}    ${50}

*** Test Cases ***
验证音量最小值-静音状态
    [Tags]    smoke    cockpit    multimedia    boundary
    [Documentation]    验证音量设置为最小值0%时，系统进入静音状态
    记录测试步骤    开始测试音量最小值边界
    # 调用通用关键字验证范围
    验证范围    ${MIN_VOLUME}    ${MIN_VOLUME}    ${MAX_VOLUME}
    # 设置音量到最小值
    Set Volume    ${MIN_VOLUME}
    # 等待总线信号响应
    等待信号响应    ${True}    timeout=10s
    # 断言当前音量等于最小值
    ${actual_volume}=    Get Current Volume
    记录测试结果    ${MIN_VOLUME}    ${actual_volume}
    Should Be Equal As Integers    ${actual_volume}    ${MIN_VOLUME}
    # 验证静音状态（音量0=静音）
    Verify Mute State    True

验证音量最大值-最大声压
    [Tags]    smoke    cockpit    multimedia    boundary
    [Documentation]    验证音量设置为最大值100%时，系统达到最大声压
    记录测试步骤    开始测试音量最大值边界
    # 调用通用关键字验证范围
    验证范围    ${MAX_VOLUME}    ${MIN_VOLUME}    ${MAX_VOLUME}
    # 设置音量到最大值
    Set Volume    ${MAX_VOLUME}
    # 等待总线信号响应
    等待信号响应    ${True}    timeout=10s
    # 断言当前音量等于最大值
    ${actual_volume}=    Get Current Volume
    记录测试结果    ${MAX_VOLUME}    ${actual_volume}
    Should Be Equal As Integers    ${actual_volume}    ${MAX_VOLUME}
    # 验证非静音状态
    Verify Mute State    False

验证音量边界值-步进为1
    [Tags]    regression    cockpit    multimedia
    [Documentation]    验证从最小值+1和最大值-1的步进正确性
    记录测试步骤    测试音量步进边界
    # 从0加到1
    Set Volume    ${MIN_VOLUME}
    Increase Volume
    ${vol_after_inc}=    Get Current Volume
    Should Be Equal As Integers    ${vol_after_inc}    1
    # 从100减到99
    Set Volume    ${MAX_VOLUME}
    Decrease Volume
    ${vol_after_dec}=    Get Current Volume
    Should Be Equal As Integers    ${vol_after_dec}    99

验证设置非法音量值应失败
    [Tags]    negative    cockpit    multimedia
    [Documentation]    验证设置-1和101等非法值时应抛出异常
    记录测试步骤    测试非法音量值拒绝
    # 设置负数应失败
    Run Keyword And Expect Error    *小于最小值*    Set Volume    -1
    # 设置超范围应失败
    Run Keyword And Expect Error    *大于最大值*    Set Volume    101

*** Keywords ***
初始化测试环境
    Log    初始化IVI模拟器...    ${LOG_LEVEL_INFO}
    Set Volume    ${DEFAULT_VOLUME}

清理测试环境
    Log    清理IVI模拟器资源...    ${LOG_LEVEL_INFO}
    Set Volume    ${DEFAULT_VOLUME}

Set Volume
    [Arguments]    ${target_volume}
    [Documentation]    设置音量（Mock模式：直接更新变量；真实环境：调用CANoe）
    验证范围    ${target_volume}    ${MIN_VOLUME}    ${MAX_VOLUME}
    Log    发送CAN信号: SET_VOLUME=${target_volume}    ${LOG_LEVEL_INFO}
    # Mock模式：更新内部状态
    Set Test Variable    ${CURRENT_VOLUME}    ${target_volume}
    # 真实环境取消下面注释，调用CANoe COM接口：
    # Send CAN Signal    0x100    ${target_volume}

Get Current Volume
    [Documentation]    获取当前音量（Mock模式返回变量；真实环境读取IVI API）
    Log    读取当前音量: ${CURRENT_VOLUME}    ${LOG_LEVEL_DEBUG}
    RETURN    ${CURRENT_VOLUME}

Increase Volume
    [Documentation]    音量+1
    ${new_vol}=    Evaluate    min(${CURRENT_VOLUME} + 1, ${MAX_VOLUME})
    Set Volume    ${new_vol}

Decrease Volume
    [Documentation]    音量-1
    ${new_vol}=    Evaluate    max(${CURRENT_VOLUME} - 1, ${MIN_VOLUME})
    Set Volume    ${new_vol}

Verify Mute State
    [Arguments]    ${expected_mute}
    [Documentation]    验证静音状态（音量为0时静音）
    IF    ${CURRENT_VOLUME} == ${MIN_VOLUME}
        Should Be True    ${expected_mute}    msg=音量0时应为静音状态
    ELSE
        Should Not Be True    ${expected_mute}    msg=音量非0时不应为静音
    END
    Log    静音状态验证通过: expected=${expected_mute}, volume=${CURRENT_VOLUME}    ${LOG_LEVEL_INFO}



###真实接Vector 硬件环境时需要修改的地方
# Set Volume
#     [Arguments]    ${target_volume}
#     # 调用 CANoe COM 接口发送信号
#     Send CAN Signal    0x100    ${target_volume}

# Get Current Volume
#     # 从 CANoe 读取信号值
#     ${val}=    Read CAN Signal    0x100
#     RETURN    ${val}