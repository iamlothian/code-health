import com.sun.source.tree.Tree;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.util.*;

public class Main {
    public static void main(String[] args) {
        InputStream inputStream = System.in;
        OutputStream outputStream = System.out;
        InputReader in = new InputReader(inputStream);
        PrintWriter out = new PrintWriter(outputStream);
        Solution solver = new Solution();
        boolean multipleTC = false;
        int testCount = multipleTC ? Integer.parseInt(in.next()) : 1;
        for (int i = 1; i <= testCount; i++) solver.solve(in, out, i);
        out.close();
    }

    static class Solution {
        PrintWriter out;
        InputReader in;


        int[][][] dp = new int[10][25][10];
        int go(int ind, int sum, int xVal, String s) {
            if(ind == s.length()) {
                if(sum == 0) {
                    return 1;
                } else {
                    return 0;
                }
            }
            if(dp[ind][sum][xVal] != -1)
                return dp[ind][sum][xVal];
            int ans = 0;
            if(Character.isDigit(s.charAt(ind))) {
                ans += go(ind + 1, (sum * 10 + (s.charAt(ind) - '0')) % 25, xVal, s);
            } else if(s.charAt(ind) == 'X') {
                if(!(ind == 0 && s.length() != 1 && xVal == 0))
                    ans += go(ind + 1, (sum * 10 + xVal) % 25, xVal, s);
            } else {
                for(int i = 0; i < 10; i++) {
                    if(i == 0 && ind == 0 && s.length() != 1)
                        continue;
                    ans += go(ind + 1, (sum * 10 + i) % 25, xVal, s);
                }
            }
            return dp[ind][sum][xVal] = ans;
        }
        public void solve(InputReader in, PrintWriter out, int test) {
            this.out = out;
            this.in = in;
            String s = n();
            for(int i = 0; i < 10; i++) {
                for(int j = 0; j < 25; j++) {
                    Arrays.fill(dp[i][j], -1);
                }
            }
            int cntX = 0;
            for(int i = 0; i < s.length(); i++) {
                if(s.charAt(i) == 'X')
                    cntX++;
            }
            if(cntX == 0) {
                pn(go(0, 0, 0, s));
                return;
            }
            int ans = 0;
            for(int i = 0; i < 10; i++) {
                ans += go(0, 0, i, s);
            }
            pn(ans);
        }



        String n() {
            return in.next();
        }

        int ni() {
            return in.nextInt();
        }

        long nl() {
            return in.nextLong();
        }

        void pn(long zx) {
            out.println(zx);
        }

        void pn(String sz) {
            out.println(sz);
        }

        void pn(double dx) {
            out.println(dx);
        }


    }

    static class InputReader {
        private InputStream stream;
        private byte[] buf = new byte[1024];
        private int curChar;
        private int numChars;

        public InputReader(InputStream stream) {
            this.stream = stream;
        }

        public int read() {
            if (numChars == -1) {
                throw new UnknownError();
            }
            if (curChar >= numChars) {
                curChar = 0;
                try {
                    numChars = stream.read(buf);
                } catch (IOException e) {
                    throw new UnknownError();
                }
                if (numChars <= 0) {
                    return -1;
                }
            }
            return buf[curChar++];
        }

        public int nextInt() {
            return Integer.parseInt(next());
        }

        public long nextLong() {
            return Long.parseLong(next());
        }

        public String next() {
            int c = read();
            while (isSpaceChar(c)) {
                c = read();
            }
            StringBuffer res = new StringBuffer();
            do {
                res.appendCodePoint(c);
                c = read();
            } while (!isSpaceChar(c));

            return res.toString();
        }

        private boolean isSpaceChar(int c) {
            return c == ' ' || c == '\n' || c == '\r' || c == '\t' || c == -1;
        }
    }
}
