#define beta rc2
#define snapshot 20200627
%define major 6

%define _qtdir %{_libdir}/qt%{major}

Name:		qt6-qtlottie
Version:	6.7.1
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}1
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qtbase.git
Source:		qtlottie-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		http://download.qt-project.org/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qtlottie-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Group:		System/Libraries
Summary:	Qt %{major} Quick 3D
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(Qt%{major}Core)
BuildRequires:	cmake(Qt%{major}Gui)
BuildRequires:	cmake(Qt%{major}Network)
BuildRequires:	cmake(Qt%{major}Xml)
BuildRequires:	cmake(Qt%{major}Widgets)
BuildRequires:	cmake(Qt%{major}Sql)
BuildRequires:	cmake(Qt%{major}PrintSupport)
BuildRequires:	cmake(Qt%{major}OpenGL)
BuildRequires:	cmake(Qt%{major}OpenGLWidgets)
BuildRequires:	cmake(Qt%{major}DBus)
BuildRequires:	cmake(Qt%{major}Qml)
BuildRequires:	cmake(Qt%{major}QmlModels)
BuildRequires:	cmake(Qt%{major}Quick)
BuildRequires:	cmake(Qt%{major}QuickTest)
BuildRequires:	qt%{major}-cmake
BuildRequires:	qt%{major}-qtdeclarative
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	cmake(LLVM)
BuildRequires:	cmake(Clang)
# Not really required, but referenced by LLVMExports.cmake
# (and then required because of the integrity check)
BuildRequires:	%{_lib}gpuruntime
License:	LGPLv3/GPLv3/GPLv2

%description
Qt %{major} support for Lottie animations

%qt6libs Bodymovin

%prep
%autosetup -p1 -n qtlottie%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DQT_BUILD_EXAMPLES:BOOL=ON \
	-DQT_WILL_INSTALL:BOOL=ON \
	-DQT_MKSPECS_DIR:FILEPATH=%{_qtdir}/mkspecs

%build
%ninja_build -C build

%install
%ninja_install -C build
%qt6_postinstall

%files
%{_qtdir}/lib/cmake/Qt6BuildInternals/StandaloneTests/QtLottieTestsConfig.cmake
%{_qtdir}/lib/cmake/Qt6Qml/QmlPlugins/*.cmake
%{_qtdir}/qml/Qt/labs/lottieqt
