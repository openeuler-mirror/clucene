Name:            clucene
Version:         2.3.3.4
Release:         35
Summary:         CLucene is a C++ port of Lucene
License:         LGPLv2+ or ASL 2.0
URL:             http://www.sourceforge.net/projects/clucene
Source0:         clucene-core-2.3.3.4-e8e3d20.tar.xz
BuildRequires:   boost-devel cmake gawk gcc-c++ zlib-devel
Patch0000:       0000-clucene-core-2.3.3.4-pkgconfig.patch
Patch0001:       0001-clucene-core-2.3.3.4-install_contribs_lib.patch

%description
CLucene is a C++ port of Lucene: the high-performance, full-featured
text search engine written in Java. CLucene is faster than lucene
as it is written in C++.

%package core
Summary:        Core clucene module
Provides:       clucene = %{version}-%{release}

%description core
CLucene is a C++ port of Lucene. It is a high-performance, full-featured
text search engine written in C++. CLucene is faster than lucene
as it is written in C++.

%package core-devel
Summary:        Development files for clucene library
Requires:       %{name}-core = %{version}-%{release}
Requires:       %{name}-contribs-lib = %{version}-%{release}

%description core-devel
CLucene is a C++ port of Lucene. It is a high-performance, full-featured text
search engine written in C++. CLucene is faster than lucene as it is written
in C++.
This package holds the development files for clucene.

%package contribs-lib
Summary:        Language specific text analyzers for %{name}
Requires:       %{name}-core = %{version}-%{release}

%description contribs-lib
%{summary}.

%prep
%autosetup -n %{name}-core-%{version} -p1

rm -rfv src/ext/{boost/,zlib/}


%build
mkdir %{_target_platform}
cd %{_target_platform}
%{cmake} \
  -DBUILD_CONTRIBS_LIB:BOOL=ON -DLIB_DESTINATION:PATH=%{_libdir} \
  -DLUCENE_SYS_INCLUDES:PATH=%{_libdir} \
  ..
cd -

%make_build -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%check
export PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion libclucene-core)" = "%{version}"
export CTEST_OUTPUT_ON_FAILURE=1
touch src/test/CMakeLists.txt && \
make -C %{_target_platform} cl_test && \
time make -C %{_target_platform} test ARGS="--timeout 300 --output-on-failure" ||:

%post core -p /sbin/ldconfig
%postun core -p /sbin/ldconfig

%post contribs-lib -p /sbin/ldconfig
%postun contribs-lib -p /sbin/ldconfig

%files core
%doc AUTHORS ChangeLog README APACHE.license COPYING LGPL.license
%{_libdir}/{libclucene-core.so.1*,libclucene-shared.so.1*}
%{_libdir}/{libclucene-core.so.%{version},libclucene-shared.so.%{version}}
%exclude %{_libdir}/CLuceneConfig.cmake/CLuceneConfig.cmake

%files contribs-lib
%{_libdir}/libclucene-contribs-lib.so.1*
%{_libdir}/libclucene-contribs-lib.so.%{version}

%files core-devel
%dir %{_libdir}/CLucene
%{_includedir}/CLucene/
%{_includedir}/CLucene.h
%{_libdir}/libclucene*.so
%{_libdir}/CLucene/{clucene-config.h,CLuceneConfig.cmake}
%{_libdir}/pkgconfig/libclucene-core.pc


%changelog
* Sun Dec 1 2019 wangzhishun <wangzhishun1@huawei.com> - 2.3.3.4-35
- Package init
