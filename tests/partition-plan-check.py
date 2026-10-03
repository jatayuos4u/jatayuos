#!/usr/bin/env python3
"""Exercise the patched plan guard in isolation; requires g++ and patched source."""
from pathlib import Path
import subprocess, sys, tempfile
s=(Path(sys.argv[1])/'src/modules/partition/core/PartitionCoreModule.cpp').read_text()
guard=s[s.index('    // Check the entire plan'):s.index('    // The automountControl job goes')]
cpp=r'''
#include <string>
#include <vector>
#include <memory>
#include <algorithm>
#include <cassert>
#include <iostream>
using QString=std::string;
struct QStringList:std::vector<QString>{bool isEmpty()const{return empty();} bool contains(const QString&s)const{return std::find(begin(),end(),s)!=end();} QStringList&operator<<(const QString&s){push_back(s);return *this;}};
enum class FileSystem{Ntfs,BitLocker,Ext4,Fat32};
struct FS{FileSystem value;FileSystem type()const{return value;}};
struct Partition{QString path;FS fs;bool efi;const FS&fileSystem()const{return fs;}QString partitionPath()const{return path;}};
struct Table{std::vector<Partition*>parts;};
struct Device{Table*t;Table*partitionTable()const{return t;}};
namespace PartitionIterator{auto begin(Table*t){return t->parts.begin();}auto end(Table*t){return t->parts.end();}}
namespace PartUtils{bool isEfiBootable(const Partition*p){return p->efi;}}
struct Job{virtual~Job()=default;};
struct JatayuProtectedPartitionJob:Job{};
struct CreatePartitionTableJob:Job{};
struct FormatPartitionJob:Job{Partition*p;explicit FormatPartitionJob(Partition*x):p(x){}Partition*partition()const{return p;}};
struct DeletePartitionJob:Job{Partition*p;explicit DeletePartitionJob(Partition*x):p(x){}Partition*partition()const{return p;}};
struct ResizePartitionJob:Job{};
namespace Calamares{struct job_ptr:std::shared_ptr<Job>{using std::shared_ptr<Job>::shared_ptr;Job*data()const{return get();}};using JobList=std::vector<job_ptr>;}
struct DevicePtr{Device*p;Device*data()const{return p;}};
struct Info{DevicePtr immutableDevice;Calamares::JobList plan;const Calamares::JobList&jobs()const{return plan;}};
Calamares::JobList check(std::vector<Info*>m_deviceInfos){
'''+guard+r'''
return {};
}
int main(){
Partition win{"/dev/nvme0n1p3",{FileSystem::Ntfs},false},esp{"/dev/nvme0n1p1",{FileSystem::Fat32},true},root{"/dev/nvme0n1p4",{FileSystem::Ext4},false};
Partition encrypted{"/dev/nvme0n1p6",{FileSystem::BitLocker},false};
Table table{{&win,&esp,&root,&encrypted}};Device disk{&table};Info info{{&disk},{}};
auto blocked=[&](Job*j){info.plan={Calamares::job_ptr(j)};return !check({&info}).empty();};
assert(blocked(new FormatPartitionJob(&win)));assert(blocked(new DeletePartitionJob(&win)));
assert(blocked(new FormatPartitionJob(&esp)));assert(blocked(new DeletePartitionJob(&esp)));
assert(blocked(new FormatPartitionJob(&encrypted)));assert(blocked(new DeletePartitionJob(&encrypted)));
assert(blocked(new CreatePartitionTableJob));assert(!blocked(new FormatPartitionJob(&root)));
assert(!blocked(new ResizePartitionJob));
// The preview type may already be ext4; original NTFS must still be protected.
Partition changedWin{win.path,{FileSystem::Ext4},false};assert(blocked(new FormatPartitionJob(&changedWin)));
// New Linux partition after shrinking Windows.
Partition newRoot{"/dev/nvme0n1p5",{FileSystem::Ext4},false};assert(!blocked(new FormatPartitionJob(&newRoot)));
Table blank{};Device empty{&blank};Info emptyInfo{{&empty},{Calamares::job_ptr(new CreatePartitionTableJob)}};
assert(check({&emptyInfo}).empty());
// A harmless second disk does not bypass protection on the Windows disk.
info.plan={Calamares::job_ptr(new DeletePartitionJob(&win))};assert(!check({&emptyInfo,&info}).empty());
std::cout<<"13 partition-plan fixtures PASS (isolated logic harness; full Calamares compilation pending)\n";
}
'''
with tempfile.TemporaryDirectory(prefix='jatayu-guard-') as directory:
    source=Path(directory)/'check.cpp'; binary=Path(directory)/'check'
    source.write_text(cpp)
    subprocess.run(['g++','-std=c++17','-Wall','-Wextra','-Werror',str(source),'-o',str(binary)],check=True)
    subprocess.run([str(binary)],check=True)
