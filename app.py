import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ScrollView } from 'react-native';

const BaccaratAnalyzer = () => {
  const [history, setHistory] = useState([]); // 게임 기록 저장

  // 1. 핵심 로직: 5칸 기준 꺾기 및 새로운 열 이동
  const renderGrid = () => {
    let columns = [[]];
    let currentCol = 0;

    history.forEach((res, index) => {
      const prevRes = history[index - 1];
      
      // 결과가 바뀌면 새 열로 이동
      if (prevRes && res !== prevRes) {
        currentCol++;
        columns[currentCol] = [];
      } 
      // 결과가 같은데 5칸이 다 찼으면 옆으로 꺾기(새 열로 이동)
      else if (columns[currentCol].length >= 5) {
        currentCol++;
        columns[currentCol] = [];
      }
      
      columns[currentCol].push(res);
    });

    return (
      <ScrollView horizontal contentContainerStyle={styles.gridContainer}>
        {columns.map((col, i) => (
          <View key={i} style={styles.column}>
            {col.map((item, j) => (
              <View key={j} style={[styles.circle, { backgroundColor: item === 'B' ? '#E74C3C' : '#3498DB' }]}>
                <Text style={styles.circleText}>{item}</Text>
              </View>
            ))}
          </View>
        ))}
      </ScrollView>
    );
  };

  return (
    <View style={styles.container}>
      {/* 상단: 추천 베팅 */}
      <View style={styles.header}>
        <Text style={styles.recommendation}>플레이어 15,000원 배팅</Text>
      </View>

      {/* 중앙: 기록판 */}
      <View style={styles.boardArea}>{renderGrid()}</View>

      {/* 메인 버튼: 가로 배치 및 크기 확대 */}
      <View style={styles.mainButtonRow}>
        <TouchableOpacity style={[styles.betBtn, styles.playerBtn]} onPress={() => setHistory([...history, 'P'])}>
          <Text style={styles.btnText}>플레이어</Text>
        </TouchableOpacity>
        <TouchableOpacity style={[styles.betBtn, styles.bankerBtn]} onPress={() => setHistory([...history, 'B'])}>
          <Text style={styles.btnText}>뱅커</Text>
        </TouchableOpacity>
      </View>

      {/* 하단: 기능 버튼 (카메라, 취소, 리셋) */}
      <View style={styles.bottomBar}>
        <TouchableOpacity style={styles.iconBtn}><Text>📸</Text></TouchableOpacity> {/* 카메라 */}
        <TouchableOpacity style={styles.subBtn} onPress={() => setHistory(history.slice(0, -1))}><Text>취소</Text></TouchableOpacity>
        <TouchableOpacity style={styles.subBtn} onPress={() => setHistory([])}><Text>리셋</Text></TouchableOpacity>
        <View style={{ width: 40 }} /> {/* 우측 이모티콘 제거된 빈 공간 */}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#121212', padding: 20 },
  header: { height: 100, justifyContent: 'center', alignItems: 'center', borderWeight: 2, borderColor: '#F1C40F', borderRadius: 10, marginBottom: 20 },
  recommendation: { fontSize: 24, color: '#F1C40F', fontWeight: 'bold' },
  boardArea: { height: 200, backgroundColor: '#FFFFFF', borderRadius: 10, padding: 10 },
  gridContainer: { flexDirection: 'row' },
  column: { width: 35, flexDirection: 'column' },
  circle: { width: 30, height: 30, borderRadius: 15, justifyContent: 'center', alignItems: 'center', margin: 2 },
  circleText: { color: 'white', fontWeight: 'bold', fontSize: 12 },
  mainButtonRow: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 30 },
  betBtn: { flex: 1, height: 80, borderRadius: 15, justifyContent: 'center', alignItems: 'center', marginHorizontal: 5 },
  playerBtn: { backgroundColor: '#2980B9' },
  bankerBtn: { backgroundColor: '#C0392B' },
  btnText: { color: 'white', fontSize: 20, fontWeight: 'bold' },
  bottomBar: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginTop: 'auto' },
  iconBtn: { width: 50, height: 50, backgroundColor: '#444', borderRadius: 25, justifyContent: 'center', alignItems: 'center' },
  subBtn: { padding: 15, backgroundColor: '#333', borderRadius: 10 },
});

export default BaccaratAnalyzer;
