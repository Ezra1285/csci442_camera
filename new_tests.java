
@Test
void testOne(){
   assertEquals("3\n",executeProgram("for(x in [1,2,3]){if(x>=3){print(x)}}"));
}

@Test 
void testTwo(){
    assertEquals("10\n",executeProgram("var y = 10 \nif(1==1){print(y)}"));

}

@Test 
void testThree(){
    assertEquals("2\n3\n4\n",executeProgram("for(x in [1,2,3]){x = x+1 \nprint(x)}"));
}
