from csp import *
import itertools
from collections import OrderedDict
from operator import itemgetter


class KenKen(CSP):

    def __init__(self,args,Domain,m_c):

        self.Table={}
        Rows=[]
        Columns=[]
        self.N=args[0]
        self.CliqueDict={}
        self.Neighbors={}
        self.min_conf=m_c
        Cliques = args[1]
        for i in range (0,self.N): 
            Rows.append([])  
            Columns.append([])    
            for j in range (0,self.N):        
                self.Table[str(i)+str(j)]="."
                Rows[i].append(str(i)+str(j))
                Columns[i].append(str(j)+str(i))

        for i in range (0,self.N):
            for j in range (0,self.N):
                n = set(Rows[i] + Columns[j])
                n.remove(str(i)+str(j))      
                self.Neighbors[str(i)+str(j)]=list(n)

        
        for c in Cliques:
            for n in c[2]:
                self.CliqueDict[n]=c
         
        self.Possible_Values=""

        for i in range(1,self.N+1):
            self.Possible_Values+=str(i)
        
        CSP.__init__(self,None,Domain, self.Neighbors,different_values_constraint)

    #BT+MRV
    def num_legal_values(self,csp, var, assignment):

        return count(self.nconflicts2(var, val, assignment) == 0
            for val in self.domains[var])

    #FC+MRV
    def num_legal_values2(self,csp, var, assignment):
        if csp.curr_domains:
            return len(csp.curr_domains[var])
        else:
            return count(self.nconflicts2(var, val, assignment) == 0
                         for val in csp.domains[var])

    def nconflicts2(self, var, val, assignment):

        def conflict(var2):
            return (var2 in assignment and
                    not self.constraints(var, val, var2, assignment[var2]))
        return count(conflict(v) for v in self.neighbors[var])

    #MRV gia to FC
    def mrv2(self,assignment, csp):

        l=[]
        for v in self.variables:
            if v not in assignment:
                l.append([v,self.num_legal_values2(csp,v,assignment)])

        mrvlist = sorted(l,key=itemgetter(1))
        return mrvlist[0][0]
 
    #to mrv dn fernei tuxaia metavlith se periptwsh isopalias alla thn metavlhth pou einai
    #mikroterh le3ikografika px 01<02 etsi wste na trexoume to idio senario
    #MRV gia to BT    
    def mrv(self,assignment, csp):

        l=[]
        for v in self.variables:
            if v not in assignment:
                l.append([v,self.num_legal_values(csp,v,assignment)])

        mrvlist = sorted(l,key=itemgetter(1))
        return mrvlist[0][0]
    

    def conflict(self,var2,var,val,assignment):
        return (var2 in assignment and
                not self.constraints(var, val, var2, assignment[var2]))
    
    #override gia na prosarmostei h cliqueConstraint
    def nconflicts(self, var, val, assignment):
        cliqueConflict=0
        conflicts=count(self.conflict(v,var,val,assignment) for v in self.neighbors[var])
        if(conflicts==0):
            if(self.CliquesConstraint(var,val,assignment) == True):
                cliqueConflict=1

        total_conf = conflicts + cliqueConflict
        return total_conf

    #ektupwsh tou table
    def PrintGrid(self,Table):
        
        return(Table)

    
    # o periorismos gia tis klikes
    def CliquesConstraint(self,var,val,assignment):

        c_domains=None
        #o min_conflicts den 8eloume na xrisimopoiei to cur_domains
        if(self.min_conf==1):
            c_domains = self.neighbors

        if(self.curr_domains==None and self.min_conf==0):
            return False

        if(self.min_conf==0):
            c_domains = self.curr_domains

        cl = self.CliqueDict[var]
        NotAssignedYet=[]
        CliqueMemberValues=[int(val)]

        for id in cl[2]:
            if(id not in assignment and id!=var):
                ValidPossValues=[]
                #gia ka8e melos ths klikas pera tou e3etazomenou 8a vroume oles tis epitreptes times
                for va in self.Possible_Values:
                    if(va  in c_domains[id]):
                        ValidPossValues.append(va)
                NotAssignedYet.append(ValidPossValues)
            elif(id!=var):
                CliqueMemberValues.append(int(assignment[id]))

        if(len(NotAssignedYet)!=0):
            #dhmiourgia olwn twn pi8anwn syndiasmwn
            AllCombinations = list(itertools.product(*NotAssignedYet))
            ValuesToTest=[]
            for tup in AllCombinations:
                l=CliqueMemberValues+list(map(int,list(tup)))
                ValuesToTest.append(l)
                   
            for l in ValuesToTest:
                if(self.CalculateClique(cl[0],cl[1],l)):
                    return False
            return True
        else:
            if(self.CalculateClique(cl[0],cl[1],CliqueMemberValues)):
                return False
            return True
    #ypologismos ths klikas , an vre8ei estw kai enas sundiasmos o periorismos ikanopoieitai
    def CalculateClique(self,op,target,cl):

        if(op=="-"):
            res=max(cl);
            cl.remove(res)
            for x in cl:
                res=res-x
                if(res<target):
                    return False
            if(res==target):
                return True

        if(op=="+"):
            res=0;
            for x in cl:
                res+=x
                if(res>target):
                    return False
            if(res==target):
                return True  

        if(op=="*"):
            res=1;
            for x in cl:
                res=res*x
                if(res>target):
                    return False
            if(res==target):
                return True   

        if(op=="/"):
            res=max(cl);
            cl.remove(res)
            for x in cl:
                res=res/x
                if(res<target):
                    return False
            if(res==target):
                return True   

        if(op==None):
            if(int(cl[0])==target):
                return True

        return False


