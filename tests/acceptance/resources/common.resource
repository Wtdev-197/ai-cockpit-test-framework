*** Settings ***
Documentation    通用共享资源文件 - 跨模块复用的变量和关键字
Library           BuiltIn
Library           Collections
Library           OperatingSystem
Library           String
Library           Process

*** Variables ***
# ==================== 超时配置 ====================
${DEFAULT_TIMEOUT}        30s
${SHORT_TIMEOUT}          5s
${LONG_TIMEOUT}           60s

# ==================== 信号延迟（模拟车载总线传输）====================
${SIGNAL_DELAY}           0.5s
${RETRY_INTERVAL}         1s
${MAX_RETRIES}            3

# ==================== 座舱通用默认值 ====================
${DEFAULT_VOLUME}         50
${MIN_VOLUME}             0
${MAX_VOLUME}             100
${DEFAULT_TEMPERATURE}    22.5
${DEFAULT_BRIGHTNESS}     70

# ==================== 路径配置 ====================
${PROJECT_ROOT}           ${EXECDIR}
${TEST_DATA_DIR}          ${PROJECT_ROOT}${/}data
${OUTPUT_DIR}             ${PROJECT_ROOT}${/}results
${RAW_DATA_DIR}           ${TEST_DATA_DIR}${/}raw

# ==================== 日志级别 ====================
${LOG_LEVEL_INFO}         INFO
${LOG_LEVEL_DEBUG}        DEBUG
${LOG_LEVEL_WARN}         WARN

*** Keywords ***
等待信号响应
    [Arguments]    ${condition}    ${timeout}=${DEFAULT_TIMEOUT}    ${retry}=${SHORT_TIMEOUT}
    [Documentation]    等待CAN/IVI信号响应，超时则失败（车载测试核心关键字）
    Wait Until Keyword Succeeds    ${timeout}    ${retry}    Should Be True    ${condition}
    Log    信号响应成功，条件满足: ${condition}    ${LOG_LEVEL_INFO}

重试执行关键字
    [Arguments]    ${keyword}    @{args}
    [Documentation]    重试执行指定关键字，最多${MAX_RETRIES}次（应对车载信号偶尔丢包）
    FOR    ${i}    IN RANGE    ${MAX_RETRIES}
        ${result}    ${msg}=    Run Keyword And Ignore Error    ${keyword}    @{args}
        IF    '${result}' == 'PASS'
            Log    关键字 ${keyword} 第 ${i+1} 次执行成功    ${LOG_LEVEL_INFO}
            RETURN
        END
        Log    第 ${i+1} 次执行失败: ${msg}，等待 ${RETRY_INTERVAL} 后重试...    ${LOG_LEVEL_WARN}
        Sleep    ${RETRY_INTERVAL}
    END
    Fail    关键字 "${keyword}" 在 ${MAX_RETRIES} 次重试后仍然失败

记录测试步骤
    [Arguments]    ${step_desc}
    [Documentation]    记录带时间戳的测试步骤（方便排查车载测试时序问题）
    ${timestamp}    Get Time    format=%Y-%m-%d %H:%M:%S.%f
    Log    [${timestamp}] ▶ ${step_desc}    ${LOG_LEVEL_INFO}

记录测试结果
    [Arguments]    ${expected}    ${actual}
    [Documentation]    记录预期值与实际值的对比
    Log    预期: ${expected}    ${LOG_LEVEL_INFO}
    Log    实际: ${actual}    ${LOG_LEVEL_INFO}
    Should Be Equal    ${expected}    ${actual}    msg=预期值与实际值不匹配！

确保输出目录存在
    [Documentation]    确保测试报告和日志目录已创建
    Create Directory    ${OUTPUT_DIR}
    Create Directory    ${OUTPUT_DIR}${/}logs
    Log    输出目录已就绪: ${OUTPUT_DIR}    ${LOG_LEVEL_DEBUG}

清理临时文件
    [Documentation]    清理测试生成的临时文件（每次测试后调用）
    Run Keyword And Ignore Error    Remove Files    ${OUTPUT_DIR}${/}temp_*
    Log    临时文件清理完成    ${LOG_LEVEL_DEBUG}

格式化CAN信号ID
    [Arguments]    ${signal_id}
    [Documentation]    将CAN信号ID格式化为十六进制字符串（如 0x100）
    ${hex_id}=    Convert To Hex    ${signal_id}
    ${formatted}=    Set Variable    0x${hex_id}
    RETURN    ${formatted}

验证范围
    [Arguments]    ${value}    ${min}    ${max}
    [Documentation]    验证数值是否在合理范围内（音量、温度等）
    Should Be True    ${value} >= ${min}    msg=值 ${value} 小于最小值 ${min}
    Should Be True    ${value} <= ${max}    msg=值 ${value} 大于最大值 ${max}
    Log    值 ${value} 在范围 [${min}, ${max}] 内 ✓    ${LOG_LEVEL_INFO}