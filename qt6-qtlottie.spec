%define beta beta2
#define snapshot 20200627
%define major 6

%define _qtdir %{_libdir}/qt%{major}

Name:		qt6-qtlottie
Version:	6.10.0
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
BuildRequires:	cmake(Qt%{major}GuiPrivate)
BuildRequires:	cmake(Qt%{major}GuiTools)
BuildRequires:	cmake(Qt%{major}Network)
BuildRequires:	cmake(Qt%{major}Xml)
BuildRequires:	cmake(Qt%{major}Widgets)
BuildRequires:	cmake(Qt%{major}Sql)
BuildRequires:	cmake(Qt%{major}Svg)
BuildRequires:	cmake(Qt%{major}PrintSupport)
BuildRequires:	cmake(Qt%{major}OpenGL)
BuildRequires:	cmake(Qt%{major}OpenGLWidgets)
BuildRequires:	cmake(Qt%{major}DBus)
BuildRequires:	cmake(Qt%{major}Qml)
BuildRequires:	cmake(Qt%{major}QmlModels)
BuildRequires:	cmake(Qt%{major}Quick)
BuildRequires:	cmake(Qt%{major}QuickControls2)
BuildRequires:	cmake(Qt%{major}QuickPrivate)
BuildRequires:	cmake(Qt%{major}QuickTest)
BuildRequires:	cmake(Qt%{major}QuickVectorImage)
BuildRequires:	cmake(Qt%{major}QuickVectorImageHelpers)
BuildRequires:	cmake(Qt%{major}QuickVectorImageGeneratorPrivate)
BuildRequires:	cmake(Qt%{major}QuickShapesPrivate)
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

%patchlist
qtlottie-6.10-workaround-cmakefile-breakage.patch

%description
Qt %{major} support for Lottie animations

%package examples
Summary:	Example files demonstrating the use of %{name}
Group:		Documentation

%description examples
Example files demonstrating the use of %{name}

%files examples
%{_qtdir}/examples/*

%global extra_files_Lottie \
%dir %{_qtdir}/plugins/vectorimageformats \
%{_qtdir}/plugins/vectorimageformats/libqlottievectorimage.so

%global extra_devel_files_Lottie \
%{_qtdir}/bin/lottietoqml \
%{_qtdir}/sbom/*

%global extra_devel_files_LottieVectorImageGenerator \
%{_qtdir}/lib/cmake/Qt6QuickVectorImageGeneratorPrivate

%qt6libs Lottie LottieVectorImageGenerator LottieVectorImageHelpers

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
