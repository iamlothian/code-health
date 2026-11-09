import java.io.*;
import java.util.*;

public class Codeforces
{
    public static void main(String args[])throws Exception
    {
        BufferedReader bu=new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb=new StringBuilder();

        char s[]=bu.readLine().toCharArray();
        boolean x=false;
        int n=s.length,i;
        for(i=0;i<n;i++) x|=s[i]=='X';

        int ans=0;
        char s2[]=new char[n];
        for(i=0;i<10;i++)
        {
            int j;
            for(j=0;j<n;j++)
            if(s[j]=='X') s2[j]=(char)('0'+i);
            else s2[j]=s[j];
            if(s2[0]=='0') continue;    //not possible

            int dp[][]=new int[2][25],cur=1,l,k;
            dp[0][0]=1;
            for(j=0;j<n;j++)
            {
                for(k=0;k<25;k++) dp[cur][k]=0;
                int lo=0,hi=9,nxt;
                if(s2[j]!='_') lo=hi=(s2[j]-'0');
                else if(s2[j]=='_' && j==0) lo++;

                for(k=0;k<25;k++)
                for(l=lo;l<=hi;l++)
                {
                    nxt=(k*10+l)%25;
                    dp[cur][nxt]+=dp[cur^1][k];
                }
                cur^=1;
            }

            ans+=dp[cur^1][0];
            if(!x) break;
        }

        if(n==1 && (s[0]=='_' || s[0]=='X' || s[0]=='0')) ans++;
        System.out.println(ans);
    }
}